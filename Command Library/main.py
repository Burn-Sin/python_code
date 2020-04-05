import json,os


def remove_block(name):
    dtc = lod_data('./data/data.json')
    if (name in dtc):
        del dtc[name]
        save_data('./data/data.json', json.dumps(dtc))

def add_block(name,data):

    try:
        dtc = lod_data('./data/data.json')
        if (name in dtc):
            dtc[name].append(data)
            save_data('./data/data.json', json.dumps(dtc))
        else:
            block = {}
            if (os.path.exists('./data/data.json')==True):
                dtc.update({name:[data]})
                block = dtc
            else:
                block = {
                    name: [data]
                }
            save_data('./data/data.json', json.dumps(block))

    except:
        block = {
            name: [data]
        }
        save_data('./data/data.json', json.dumps(block))

def lod_data(file_name):
    try:
        with open(file_name,'r',encoding='utf-8') as F:
            data = json.loads(F.read())
            return data
    except:
        pass

def save_data(file_name,data):
    with open(file_name,'w',encoding = "utf-8") as F:
        F.write(data)

def main():
    #add_block('yyy','saandasd'+'\n'+'1111')
    #print(lod_data('./data/data.json'))
    #remove_block('yyy')
    while True:
        command = input('>').split(maxsplit=1)
        if (len(command) == 0):
            pass
        else:
            C = command[0]
            if (C == 'list'):
                try:
                    dct = lod_data('./data/data.json')  # values()
                    for s in dct:
                        print(s)
                except:
                    pass
        if (len(command)==2):
            S = command[1]
            if (S == '-n'):
                print('set a new block!')
                while True:
                    td = input(C + '->')
                    if (len(td) == 0):
                        pass
                    elif (td == '-q'):
                        C = ''
                        break
                    else:
                        add_block(C, td)
            elif (S == '-d'):
                print('remove a block!')
                remove_block(C)

        try:
            dct = lod_data('./data/data.json')  # values()
            for l in dct[C]:
                print(l)
        except:
            pass
        C = ''









    #if (isinstance(command,str)):print('1111')


if __name__ == '__main__':
    main()
