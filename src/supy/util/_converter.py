#!/usr/bin/env python
########################################################
# Table Converter for SUEWS
# Ting Sun, ting.sun@reading.ac.uk
# Yihao Tang, Yihao.Tang@student.reading.ac.uk
# history:
# TS, 13 Oct 2017: initial version
# YT, 01 Jun 2018: added the chained conversion
# TS, 21 May 2019: integrated into supy
########################################################
# %%
import os
import os.path
import sys
# ignore warnings raised by numpy when reading-in -9 lines
import warnings
from collections import defaultdict
from fnmatch import fnmatch
from heapq import heappop, heappush
from pathlib import Path
from shutil import copyfile, copytree, move,rmtree

import f90nml
import numpy as np
import pandas as pd

from .._env import path_supy_module
from .._load import load_SUEWS_nml
from .._misc import path_insensitive

warnings.filterwarnings('ignore')
########################################################
# %%
# load the rule file
rules = pd.read_csv(path_supy_module/'util'/'rules.csv')
list_ver_from = rules['From'].unique().tolist()
list_ver_to = rules['To'].unique().tolist()
# str_rules = rules.stack().str.decode('utf-8').unstack()
# for col in str_rules:
#     rules[col] = str_rules[col]

# %%
########################################################
# define action functions:
# the current supported actions:
# rename, delete, add, move


# rename:
# rename file
def rename_file(toFile, toVar, toCol, toVal):
    # toVar, toCol are ignored
    if not Path(toFile).exists():
        print(toFile, 'not exiting')
        sys.exit()
    else:
        dir = Path(toFile).resolve().parent
        path_toFile_renamed = dir/toVal
        os.rename(toFile, path_toFile_renamed)


# rename variable
def rename_var(toFile, toVar, toCol, toVal):
    # if namelist:
    if toFile.endswith('.nml'):
        print(toFile, toVar, toVal)
        rename_var_nml(toFile, toVar, toVal)
    else:
        dataX = np.genfromtxt(toFile, dtype=np.ndarray, skip_header=1,
                              comments='!', names=True, invalid_raise=False)
        # generate headers
        header = np.array(dataX.dtype.names)
        header[header == toVar] = toVal
        headerLine = ' '.join(
            str(i + 1)
            for i in np.arange(len(dataX[0]))) + '\n' + ' '.join(header)

        # convert to a more handy array
        dataX = np.array(dataX.tolist()).astype(str)

        # NB: caveat: comment info will be dropped, needs to be recovered
        np.savetxt(toFile, dataX, fmt='%s', header=headerLine,
                   footer='-9\n-9', comments='')

        # print toVar + ' has been renamed to ' + toVal + '!'
        return


def rename_var_nml(toFile, toVar, toVal):
    nml = f90nml.read(toFile)
    title = list(nml.keys())[0]
    if (toVar.lower() in nml[title].keys()):
        nml[title][toVal] = nml[title].pop(toVar)
    else:
        print(toVar + ' does not exist!')
    nml.write(toFile, force=True)


# delete:
# delete variable
def delete_var(toFile, toVar, toCol, toVal):
    if toFile.endswith('.nml'):
        delete_var_nml(toFile, toVar, toVal)
    else:
        dataX = np.genfromtxt(toFile, dtype=np.ndarray, skip_header=1,
                              comments='!', invalid_raise=False)

        # convert to a more handy array
        dataX = np.array(dataX.tolist()).astype(str)
        # print dataX

        # position of columns to delete
        posDel = np.where(dataX[0] == toVar)
        # print posDel
        dataX = np.delete(dataX, posDel, axis=1)

        # dataX[0] = [str(i + 1) for i in np.arange(len(dataX[0]))]
        headerLine = ' '.join(str(i + 1)
                              for i in np.arange(len(dataX[0])))
        # NB: caveat: comment info will be dropped, needs to be recovered
        np.savetxt(toFile, dataX, fmt='%s', header=headerLine,
                   footer='-9\n-9', comments='')

        # print toVar + ' has been deleted!'
        return


def delete_var_nml(toFile, toVar, toVal):
    nml = f90nml.read(toFile)
    toVarX = toVar.lower()
    title = list(nml.keys())[0]
    if (toVarX in nml[title].keys()):
        nml[title].pop(toVarX)
    else:
        print(toVar + ' does not exist!')
    nml.write(toFile, force=True)


# add:
# add variable(s) to a file
def add_var(toFile, toVar, toCol, toVal):
    # toFile missing
    if not(os.path.isfile(toFile)):
        # create toFile
        dataX = [1]
        np.savetxt(toFile, dataX, header='1\nCode',
                   footer='-9\n-9', fmt='%s', comments='')

    # if namelist:
    if toFile.endswith('.nml'):
        add_var_nml(toFile, toVar, toVal)
    else:
        # load original data from toFile
        dataX = pd.read_csv(
            toFile,
            header=1,
            delim_whitespace=True,
            comment='!',
        )
        # construct new column
        colNew = np.empty(dataX.shape[0], dtype=np.object)
        colNew = toVal
        # insert new column
        dataX.insert(int(toCol) - 1, toVar, colNew)
        # save new file
        ind = np.arange(dataX.shape[1])+1
        col_name = dataX.columns
        col_new = pd.MultiIndex.from_arrays(
            [ind, col_name]
        )
        dataX.columns = col_new
        dataX.iloc[-2:] = np.nan
        dataX.iloc[-2:, 0] = -9
        dataX.iloc[:, 0] = dataX.iloc[:, 0].astype(int)
        dataX.to_csv(
            toFile,
            sep=' ',
            float_format='%10.4f',
            quotechar=' ',
            index=False,
        )


def add_var_nml(toFile, toVar, toVal):
    nml = f90nml.read(toFile)
    toVarX = toVar.lower()
    title = list(nml.keys())[0]
    if not(toVarX in nml[title].keys()):
        nml[title][toVarX] = toVal
    else:
        print(toVar + ' exists!')
    nml.write(toFile, force=True)


def change_var_nml(toFile, toVar, toVal):
    nml = f90nml.read(toFile)
    nml[toVar] = toVal
    nml.write(toFile)


# a single conversion between two versions
def SUEWS_Converter_single(fromDir, toDir, fromVer, toVer):
    # copy files in fromDir to toDir, only: *.nml, SUEWS_*.txt
    if os.path.exists(toDir) is False:
        os.mkdir(toDir)
    fileList = []
    for fileX in os.listdir(fromDir):
        if any(fnmatch(fileX, p) for p in ['SUEWS*.txt', '*.nml']):
            fileList.append(fileX)

    for fileX in fileList:
        copyfile(os.path.join(fromDir, fileX), os.path.join(toDir, fileX))

    # list all files involved in the given conversion
    posRules = np.unique(
        np.where(
            np.array(rules.loc[:, ['From', 'To']].values.tolist()) == [fromVer, toVer])[0])
    filesToConvert = np.unique(rules['File'][posRules])
    # print('posRules', posRules,
    #       rules.loc[:, ['From', 'To']],
    #       np.array(rules.loc[:, ['From', 'To']].values),
    #       [fromVer, toVer])
    print('filesToConvert', filesToConvert)

    for fileX in filesToConvert:
        print('working on file:', fileX)
        actionList = rules.values[posRules].compress(
            rules['File'].values[posRules] == fileX, axis=0)
        actionList = actionList[:, 2:]
        # actionList = np.array(actionList.tolist())[:, 2:].astype('S140')
        # prepend toDir to fileX
        actionList[:, 1] = os.path.join(toDir, fileX)
        # print('actionList:', actionList)
        SUEWS_Converter_file(os.path.join(toDir, fileX), actionList)


def SUEWS_Converter_file(fileX, actionList):
    # actionList:[Action,File,Variable,Column,Value]
    # for a given fileX, action order:
    # 1. rename
    # 2. delete
    # 3. move
    # 4. add
    # 5. rename file
    order = {
        'Keep': 0,
        'Rename': 1,
        'Delete': 2,
        'Move': 3,
        'Add': 4,
        'Rename_File': 5,
    }

    todoList = np.array(
        [np.concatenate(([order[x[0]]], x)).tolist() for x in actionList])
    # print('todoList:\n', todoList, '\n')
    # sort by Column number, then by Action order in actionList; also expand
    # dtype size
    todoList = todoList[np.lexsort(
        (todoList[:, 4].astype(int), todoList[:, 0]))][:, 1:]

    # print todoList,fileX
    # correct file names with proper path
    todoList[:, 1] = fileX
    # print todoList,fileX
    for action in todoList:
        # print(action)
        SUEWS_Converter_action(*action)


def keep_file(toFile, var, col, val):
    pass


def SUEWS_Converter_action(action, toFile, var, col, val):
    print(action, toFile, var, col, val)
    actionFunc = {
        'Rename': rename_var,
        'Delete': delete_var,
        'Add': add_var,
        'Rename_File': rename_file,
        'Keep': keep_file,
    }
    actionFunc[action](toFile, var, col, val)

    print(action + ' ' + var + ' for ' + toFile + ': done!')
    return


def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))
    q, seen = [(0, f, ())], set()

    while q:
        (cost, v1, path) = heappop(q)

        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t:
                return (cost, path)
            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + c, v2, path))

    return float("inf")


def version_list(fromVer, toVer):
    edges = []
    # a = pd.read_csv('rules.csv')
    a = rules
    v_from = np.unique(a['From'])
    for i in v_from:
        df = a[a['From'] == i]
        for k in np.unique(df['To']):
            edges.append((i, k, 1))

    s = dijkstra(edges, fromVer, toVer)
    chain_ver = []
    while s:
        chain_ver.append(s[0])
        s = s[1]
    return chain_ver


# a chained conversion across multiple versions
def convert_table(fromDir, toDir, fromVer, toVer):
    chain_ver = version_list(fromVer, toVer)
    len_chain = chain_ver[0]
    print('working on chained conversion,', f'{len_chain} actions to take')
    print('chained list:', chain_ver[1:], '\n')
    tempDir_1 = 'temp1'
    tempDir_2 = 'temp2'
    i = chain_ver[0]
    # Create temporary folders
    if os.path.exists(tempDir_1) is False:
        os.mkdir(tempDir_1)
    if os.path.exists(tempDir_2) is False:
        os.mkdir(tempDir_2)

    # flatten all file structures in tempDir_1
    # locate input folder
    ser_nml = load_SUEWS_nml(str(Path(fromDir)/'RunControl.nml')).runcontrol
    path_input = (Path(fromDir)/ser_nml['fileinputpath']).resolve()
    list_table_input = (
        [x for x in path_input.glob('SUEWS*.txt')]
        + [x for x in path_input.glob('*.nml')]
        + [x for x in Path(fromDir).resolve().glob('*.nml')]
    )
    # copy flattened files into tempDir_1 for later processing
    tempDir_1 = 'temp1'
    for fileX in list_table_input:
        copyfile(fileX.resolve(), Path(tempDir_1) / (fileX.name))
    # print(list_table_input)
    # print(tempDir_1)

    # Indirect version conversion process
    while i > 1:
        print('working on:', chain_ver[i + 1], '-->', chain_ver[i])
        if i % 2:
            tempDir_2 = 'temp2'
            SUEWS_Converter_single(
                tempDir_1, tempDir_2, chain_ver[i + 1], chain_ver[i])
            tempDir_1 = 'temp1'
            # Remove input temporary folders
            rmtree(tempDir_1, ignore_errors=True)

        else:
            tempDir_1 = 'temp1'
            SUEWS_Converter_single(
                tempDir_2, tempDir_1, chain_ver[i + 1], chain_ver[i])
            tempDir_2 = 'temp2'
            # Remove input temporary folders
            rmtree(tempDir_2, ignore_errors=True)
            # this loop always break in this part
        i -= 1

    print('working on:', chain_ver[i + 1], '-->', chain_ver[i])
    SUEWS_Converter_single(tempDir_1, toDir, chain_ver[2], chain_ver[1])
    # Remove temporary folders
    rmtree(tempDir_1, ignore_errors=True)
    rmtree(tempDir_2, ignore_errors=True)

    # cleaning and move input tables into the `input` folder
    ser_nml = load_SUEWS_nml(str(Path(toDir)/'RunControl.nml')).runcontrol

    path_input = (Path(toDir)/ser_nml['fileinputpath']).resolve()
    path_output = (Path(toDir)/ser_nml['fileoutputpath']).resolve()
    path_input.mkdir(exist_ok=True)
    path_output.mkdir(exist_ok=True)

    list_table_input = (
        [x for x in Path(toDir).glob('SUEWS*.txt')]
        + [x for x in Path(toDir).glob('*.nml') if 'RunControl' not in str(x)]
    )

    for fileX in list_table_input:
        move(fileX.resolve(), path_input / (fileX.name))



