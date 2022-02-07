#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import uuid
import io

REMOTE_CONFIG_LIST_PATH = ""
REMOTE_DEL_FLAG = "-_remove"
REMOTE_CALLBACK_SPLIT_FLAG = ""


# class MsgFormat:
#     @staticmethod
#     def remoteExistMsg(remote, reason):
#         return "ip={},port={}) already exist,(because of {}),please use [ ed (name or uuid) .. ] to modify it.".format(remote.ip, remote.port, reason)


class Remote:
    def __init__(self, isCreateNone=None):
        if(isCreateNone):
            self.uuid = ""
            self.ip = ""
            self.port = ""
            self.way = ""
            self.password = ""
            self.name = ""
            self.user = ""
        else:
            self.uuid = ''.join(str(uuid.uuid4()).split("-"))
            self.ip = ""
            self.port = "22"
            self.way = "pwd"
            self.password = ""
            self.name = ""
            self.user = "root"

    def s_uuid(self, uuid):
        self.uuid = uuid
        return self

    def s_ip(self, ip):
        self.ip = ip
        return self

    def s_port(self, port):
        self.port = port
        return self

    def s_way(self, way):
        self.way = way
        return self

    def s_password(self, password):
        self.password = password
        return self

    def s_name(self, name):
        self.name = name
        return self

    def s_user(self, user):
        self.user = user
        return self

    def s_by_print(self, printStr):
        prspt = printStr.split(" ")
        self.uuid = prspt[0] if prspt[0] != "-" else self.uuid
        self.ip = prspt[1] if prspt[1] != "-" else self.ip
        self.port = prspt[2] if prspt[2] != "-" else self.port
        self.user = prspt[3] if prspt[3] != "-" else self.way
        self.way = prspt[4] if prspt[4] != "-" else self.password
        self.password = prspt[5] if prspt[5] != "-" else self.name
        self.name = prspt[6] if prspt[6] != "-" else self.user
        return self

    def to_print(self):
        if(self.uuid == REMOTE_DEL_FLAG):
            return ""
        self.name = self.uuid if len(self.name) <= 0 else self.name
        uuidstr = self.uuid if len(self.uuid) >= 0 else ''.join(
            str(uuid.uuid4()).split("-"))
        ip = self.ip if len(self.ip) >= 0 else '-'
        port = self.port if len(self.port) >= 0 else '22'
        way = self.way if len(self.way) >= 0 else 'pwd'
        password = self.password if len(self.password) >= 0 else '-'
        name = self.name if len(self.name) >= 0 else uuidstr
        user = self.user if len(self.user) >= 0 else 'root'
        return uuidstr+" "+ip+" "+port+" "+user+" "+way+" "+password+" "+name+"\n"


class RemoteConfigListFile:

    @staticmethod
    def getRemoteConfigFile(file):
        file.seek(0)
        return file

    @staticmethod
    def addRemoteToWrite(remote: Remote):
        with open(REMOTE_CONFIG_LIST_PATH, 'r') as file:
            lines = file.readlines()
            lines.append(remote.to_print())
            RemoteConfigListFile.writeRemoteConfigFile(lines)

    @staticmethod
    def writeRemoteConfigFile(remotes: list):
        with open(REMOTE_CONFIG_LIST_PATH, 'w') as file:
            file.writelines(remotes)

    @staticmethod
    def isExistRemote(remote: Remote, changeOnExist):
        def checkCallBack(back, fRemote):
            if(back is not None):
                back(fRemote)
        try:
            with open(REMOTE_CONFIG_LIST_PATH, 'r') as file:
                lines = file.readlines()
                for i in range(0, len(lines)):
                    line = lines[i].replace("\n", "")
                    if(len(line) <= 0):
                        continue
                    fRemote = Remote().s_by_print(line)
                    if fRemote.uuid == remote.uuid:
                        checkCallBack(changeOnExist, fRemote)
                        lines[i] = fRemote.to_print()
                        return [True, fRemote, "uuid[{}] exist".format(remote.uuid), lines]
                    elif fRemote.name == remote.name:
                        checkCallBack(changeOnExist, fRemote)
                        lines[i] = fRemote.to_print()
                        return [True, fRemote, "name[{}] exist".format(remote.name), lines]
                    elif fRemote.ip == remote.ip and fRemote.port == remote.port:
                        checkCallBack(changeOnExist, fRemote)
                        lines[i] = fRemote.to_print()
                        return [True, fRemote, "ip:port[{}:{}] exist".format(remote.ip, remote.port), lines]
        except print(0):
            print("The config file content is on error,please check it at '", REMOTE_CONFIG_LIST_PATH, "'")
            exit()
        return [False, None, "", []]


def addRemote(pArr):
    remote = Remote()
    initProperties(remote, pArr)
    findRemote = RemoteConfigListFile.isExistRemote(remote, None)
    if(findRemote[0]):
        print("ip={},port={}) already exist,(because of {}".format(remote.ip, remote.port, findRemote[2]))
        exit()
    else:
        RemoteConfigListFile.addRemoteToWrite(remote)
        print("uuid={},ip={},port={},user={},way={},password={},name={}),successfully add into remote list".format(remote.uuid, remote.ip, remote.port, remote.user, remote.way, remote.password, remote.name))


def editRemote(pArr):
    def changeRemoteCallBack(fRemote):
        initProperties(fRemote, pArr[1:len(pArr)])

    remote = Remote(1)
    if(len(pArr) <= 1 or pArr[0].find('-') >= 0):
        print("The parameter is not allow, please use uuid/name like 'lssh ed uuid/name (...editArgs)'")
    else:
        remote.s_uuid(pArr[0])
        remote.s_name(pArr[0])
        findRemote = RemoteConfigListFile.isExistRemote(
            remote, changeRemoteCallBack)
        if(findRemote[0]):
            RemoteConfigListFile.writeRemoteConfigFile(findRemote[3])
            print("uuid={},ip={},port={},user={},way={},password={},name={}) edit success.".format(findRemote[1].uuid, findRemote[1].ip, findRemote[1].port, findRemote[1].user, findRemote[1].way, findRemote[1].password, findRemote[1].name))
        else:
            print(pArr[0], " is not exist.")


def removeRemote(pArr):
    def removeRemoteCallBack(fRemote):
        fRemote.s_uuid(REMOTE_DEL_FLAG)
    remote = Remote(1)
    if(len(pArr) < 1 or pArr[0].find('-') >= 0):
        print("The parameter is not allow, please use uuid/name like 'lssh ed uuid/name'")
    else:
        remote.s_uuid(pArr[0])
        remote.s_name(pArr[0])
        findRemote = RemoteConfigListFile.isExistRemote(remote, removeRemoteCallBack)
        if(findRemote[0]):
            RemoteConfigListFile.writeRemoteConfigFile(findRemote[3])
            print("uuid={},ip={},port={},user={},way={},password={},name={}) remove success.".format(findRemote[1].uuid, findRemote[1].ip, findRemote[1].port, findRemote[1].user, findRemote[1].way, findRemote[1].password, findRemote[1].name))
        else:
            print(pArr[0], " is not exist.")


def cpRemote(pArr):
    remote = Remote(1)
    if(len(pArr) < 1 or pArr[0].find('-') >= 0 or len(pArr[1].split(':')) != 2):
        print("The parameter is not allow, please use uuid/name like 'lssh cp uuid/name source:target'")
    else:
        pathArr = pArr[1].split(':')
        sourcePath = pathArr[0]
        targetPath = pathArr[1]
        remote.s_uuid(pArr[0])
        remote.s_name(pArr[0])
        findRemote = RemoteConfigListFile.isExistRemote(remote, None)
        if(findRemote[0]):
            if(findRemote[1].way == "pk"):
                cpCmd = "scp -r -P {} -i {} {} {}@{}:{}".format(findRemote[1].port, findRemote[1].password, sourcePath, findRemote[1].user, findRemote[1].ip, targetPath)
            elif(findRemote[1].way == "pwd"):
                cpCmd = "sshpass -p {} scp -r -P {} {} {}@{}:{}".format(findRemote[1].password, findRemote[1].port, sourcePath, findRemote[1].user, findRemote[1].ip, targetPath)
            else:
                print("uuid={},ip={},port={},user={},way={},password={},name={}) way is not allowed.".format(findRemote[1].uuid, findRemote[1].ip, findRemote[1].port, findRemote[1].user, findRemote[1].way, findRemote[1].password, findRemote[1].name))
                exit()
            cpCmd = cpCmd.replace(" ", REMOTE_CALLBACK_SPLIT_FLAG)
            print("success ", cpCmd)
        else:
            print(pArr[0], " is not exist.")


def connRemote(pArr):
    remote = Remote(1)
    if(len(pArr) < 1 or pArr[0].find('-') >= 0):
        print("The parameter is not allow, please use uuid/name like 'lssh conn/co uuid/name'")
    else:
        remote.s_uuid(pArr[0])
        remote.s_name(pArr[0])
        findRemote = RemoteConfigListFile.isExistRemote(remote, None)
        if(findRemote[0]):
            if(findRemote[1].way == "pk"):
                cpCmd = "ssh -i {} {}@{} -p {}".format(findRemote[1].password, findRemote[1].user, findRemote[1].ip, findRemote[1].port)
            elif(findRemote[1].way == "pwd"):
                cpCmd = "sshpass -p {} ssh {}@{} -p {}".format(findRemote[1].password, findRemote[1].user, findRemote[1].ip, findRemote[1].port)
            else:
                print("uuid={},ip={},port={},user={},way={},password={},name={}) way is not allowed.".format(findRemote[1].uuid, findRemote[1].ip, findRemote[1].port, findRemote[1].user, findRemote[1].way, findRemote[1].password, findRemote[1].name))
                exit()
            cpCmd = cpCmd.replace(" ", REMOTE_CALLBACK_SPLIT_FLAG)
            print("success ", cpCmd)
        else:
            print(pArr[0], " is not exist.")


def inputParser(str):
    cmdsp = str.split(" ")
    if(len(cmdsp) <= 1):
        print("remote properties is not allows")
        exit()
    elif(cmdsp[0] == "ad"):
        addRemote(cmdsp[1:len(cmdsp)])
    elif(cmdsp[0] == "ed"):
        editRemote(cmdsp[1:len(cmdsp)])
    elif(cmdsp[0] == "rm"):
        removeRemote(cmdsp[1:len(cmdsp)])
    elif(cmdsp[0] == "cp"):
        cpRemote(cmdsp[1:len(cmdsp)])
    elif(cmdsp[0] == "conn") or (cmdsp[0] == "cn"):
        connRemote(cmdsp[1:len(cmdsp)])


def initProperties(remote: Remote, propertiesArr):
    for index in range(len(propertiesArr)):
        properties = propertiesArr[index]
        if(properties == "-a"):
            remote.s_ip(propertiesArr[index+1])
        if(properties == "-p"):
            remote.s_port(propertiesArr[index+1])
        if(properties == "-w"):
            remote.s_way(propertiesArr[index+1])
        if(properties == "-k"):
            remote.s_password(propertiesArr[index+1])
        if(properties == "-n"):
            remote.s_name(propertiesArr[index+1])
        if(properties == "-u"):
            remote.s_user(propertiesArr[index+1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='lssh remote config function')
    parser.add_argument('-p', '--params', type=str, help='the params for remote(from sh $*')
    parser.add_argument('-cp', '--configPath', type=str, help='the config path for remote_list.config')
    parser.add_argument('-cbsp', '--callBackSplit', type=str, help='the spilt char of callback str to spilt result and result status')
    args = parser.parse_args()
    if(args.configPath is None or len(args.configPath) == 0):
        print("remote list config path can't be empty or None")
        exit()
    REMOTE_CONFIG_LIST_PATH = args.configPath
    REMOTE_CALLBACK_SPLIT_FLAG = args.callBackSplit
    inputParser(args.params)
