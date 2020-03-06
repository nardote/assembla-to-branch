import requests
import json
import sys
import subprocess

headers = {'X-Api-Key': '', 'X-Api-Secret': ''}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def requestJson(url,header):
    #print(url)
    r = requests.get(url, headers=headers)
    jsonResponse = json.loads(r.text)
    return jsonResponse

def getIdTciket():
    #espero el id del branch
    print(bcolors.WARNING+"ID del ticket:"+bcolors.ENDC)
    return sys.stdin.readline()



def imprimirTickets(spaceId, headers):

    tickets = requestJson('https://api.assembla.com/v1/spaces/'+spaceId.strip('\n')+'/tickets?per_page=100&sort_by=id&sort_order=desc', headers)

    print("cantidad de tickets cargados: " + bcolors.OKGREEN +  str(len(tickets)) + bcolors.ENDC )
    #muestro tickets
    i = 0
    for ticket in tickets:
        if i >= 20:
            break
        print(bcolors.OKGREEN +str(ticket["number"])+bcolors.ENDC+" "+bcolors.HEADER+ticket["summary"]+bcolors.ENDC)
        i = i+1

    #hago un bucle para esperar el id seleccionado
    while True:
        idTicket = getIdTciket()

        if idTicket:
            print("Buscando ticket "+str(idTicket))
            try:
                #busco ticket
                name = ""
                ticketSeleccionado = requestJson('https://api.assembla.com/v1/spaces/'+spaceId.strip('\n')+'/tickets/'+str(idTicket)+'?per_page=1&sort_by=id&sort_order=desc', headers)

                if 'error' in ticketSeleccionado.keys():
                    print(bcolors.FAIL + "No se encontro ese ticket seleccionado" + bcolors.ENDC )
                    imprimirTickets(spaceId, headers)
                    break                    
                else:
                    name = ticketSeleccionado['summary']
                    ticketnumber = ticketSeleccionado['number']
                    

                #si tiene nombre crea el branch
                if name:
                    print(bcolors.WARNING + name.replace(" ", "-").lower() + bcolors.ENDC )

                    branchName = ""+str(ticketnumber)+"-"+name.replace(" ", "-").replace("[", "").replace("]", "").replace("\\", "").replace("/", "").lower()
                    
                    print("Se crea el branch con el nombre: " + bcolors.OKGREEN +  str(branchName) + bcolors.ENDC )
                    subprocess.run( ['git', 'checkout', '-b', branchName])
                    break
                else:
                    print(bcolors.FAIL + "No se encontro ese ticket" + bcolors.ENDC )
            except:summary




spaces = requestJson('https://api.assembla.com/v1/spaces', headers)


print(bcolors.OKGREEN + "Proyectos" + bcolors.ENDC)

#muestro proyectos
i = 0
for space in spaces:
    print(bcolors.OKGREEN + str(i)+ ") "+ bcolors.ENDC +bcolors.HEADER+space["name"]+bcolors.ENDC)
    i = i + 1

print(bcolors.WARNING+"Seleccione un proyecto:"+bcolors.ENDC)
proyecto = sys.stdin.readline()

imprimirTickets(spaces[int(proyecto)]["id"], headers)
