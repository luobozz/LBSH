#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import uuid
import io

REMOTE_CONFIG_LIST_PATH = ""


class MsgFormat:
    @staticmethod
    def remoteExistMsg(remote, reason):
        return "ip={},port={}) already exist,(because of {}),please use [ ed (name or uuid) .. ] to modify it.".format(remote.ip, remote.port, reason)


class Remote:
    def __init__(self):
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
        self.name = self.uuid if len(self.name) <= 0 else self.name
        uuidstr = self.uuid if len(self.uuid) >= 0 else ''.join(
            str(uuid.uuid4()).split("-"))
        ip = self.ip if len(self.ip) >= 0 else '-'
        port = self.port if len(self.port) >= 0 else '22'
        way = self.way if len(self.way) >= 0 else 'pwd'
        password = self.password if len(self.password) >= 0 else '-'
        name = self.name if len(self.name) >= 0 else uuidstr
        user = self.user if len(self.user) >= 0 else 'root'
        return uuidstr+" "+ip+" "+port+" "+user+" "+way+" "+password+" "+name


class RemoteConfigListFile:
    @staticmethod
    def getRemoteConfigFile():
        file = open(REMOTE_CONFIG_LIST_PATH, "w+", encoding="utf-8")
        file.seek(0)
        return file
    def setRemoteConfigFile(file,remote:Remote):
        lines=file.readlines()
        lines.append(remote.to_print())
        file.writelines(lines)

    @staticmethod
    def isExistRemote(file, remote: Remote):
        needExit=False;
        try:
            lines = file.readlines()
            for line in lines:
                line=line.replace("\n","")
                if(len(line)<=0):
                    continue
                fRemote = Remote().s_by_print(line)
                if fRemote.uuid == remote.uuid:
                    print(MsgFormat.remoteExistMsg(
                        remote, "uuid[{}] exist".format(remote.uuid)))
                    needExit=True
                    break
                elif fRemote.name == remote.name:
                    print(MsgFormat.remoteExistMsg(
                        remote, "name[{}] exist".format(remote.name)))
                    needExit=True
                    break
                elif fRemote.ip == remote.ip and fRemote.port == remote.port:
                    print(MsgFormat.remoteExistMsg(
                        remote, "ip:port[{}:{}] exist".format(remote.ip, remote.port)))
                    needExit=True
                    break
        except print(0):
            print("The config file content is on error,please check it at '",REMOTE_CONFIG_LIST_PATH,"'")
            exit()
        if(needExit):
            exit()


def addRemote(pArr):
    remote = Remote()
    initProperties(remote, pArr)
    file=RemoteConfigListFile.getRemoteConfigFile();
    RemoteConfigListFile.isExistRemote(file, remote)
    # file.write(remote.to_print()+"\n")
    RemoteConfigListFile.setRemoteConfigFile(file,remote)
    print("uuid={},ip={},port={},user={},way={},password={},name={}),successfully add into remote list".format(remote.uuid,remote.ip,remote.port,remote.user,remote.way,remote.password,remote.name))


def editRemote(pArr):
    remote=Remote()
    initProperties(remote, pArr)
    print(remote)
    # print("ed", pArr)


def removeRemote(pArr):
    print("rm", pArr)


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
    parser.add_argument('-p', '--params', type=str,
                        help='the params for remote(from sh $*')
    parser.add_argument('-cp', '--configPath', type=str,
                        help='the config path for remote_list.config')
    args = parser.parse_args()
    if(args.configPath is None or len(args.configPath) == 0):
        print("remote list config path can't be empty or None")
        exit()
    REMOTE_CONFIG_LIST_PATH = args.configPath
    inputParser(args.params)
