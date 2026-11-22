#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NXT27 · Neural eXecution Terminal — edición CLI (corre dentro de tu terminal).
Uso:
  curl -fsSL https://raw.githubusercontent.com/s0k1x/Neural-eXecution-Terminal-NXT27/main/nxt27.py -o /tmp/nxt27.py && python3 /tmp/nxt27.py
Solo stdlib. Herramientas reales (hash, subred, jwt, ping) + recon simulado/educativo.
"""
import sys, os, hashlib, base64, binascii, ipaddress, platform, subprocess, getpass, uuid, secrets, math, shutil, json, time

V="\033[1;35m"; VB="\033[95m"; D="\033[90m"; G="\033[92m"; Y="\033[93m"; R="\033[91m"; C="\033[96m"; N="\033[0m"
USER=getpass.getuser() or "root"; HOST=platform.node() or "nxt27"

BANNER = VB + r"""
 ███╗   ██╗██╗  ██╗████████╗██████╗ ███████╗
 ████╗  ██║╚██╗██╔╝╚══██╔══╝╚════██╗╚════██║
 ██╔██╗ ██║ ╚███╔╝    ██║    █████╔╝    ██╔╝
 ██║╚██╗██║ ██╔██╗    ██║   ██╔═══╝    ██╔╝
 ██║ ╚████║██╔╝ ██╗   ██║   ███████╗   ██║
 ╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚══════╝   ╚═╝""" + N

FONT={'A':["█▀█","█▀█","▀ ▀"],'B':["█▀▄","█▀▄","▀▀ "],'C':["█▀▀","█  ","▀▀▀"],'D':["█▀▄","█ █","▀▀ "],'E':["█▀▀","█▀▀","▀▀▀"],'F':["█▀▀","█▀▀","▀  "],'G':["█▀▀","█ █","▀▀▀"],'H':["█ █","█▀█","▀ ▀"],'I':["█","█","▀"],'J':["  █","  █","▀▀ "],'K':["█ █","█▀▄","▀ ▀"],'L':["█  ","█  ","▀▀▀"],'M':["█▄█","█▀█","▀ ▀"],'N':["█▄█","█▀█","▀ ▀"],'O':["█▀█","█ █","▀▀▀"],'P':["█▀█","█▀▀","▀  "],'Q':["█▀█","█ █","▀▀█"],'R':["█▀█","█▀▄","▀ ▀"],'S':["█▀▀","▀▀█","▀▀▀"],'T':["▀█▀"," █ "," ▀ "],'U':["█ █","█ █","▀▀▀"],'V':["█ █","█ █"," ▀ "],'W':["█ █","█▀█","▀ ▀"],'X':["█ █"," █ ","▀ ▀"],'Y':["█ █"," █ "," ▀ "],'Z':["▀▀█"," █ ","▀▀▀"],'0':["█▀█","█ █","▀▀▀"],'1':["▀█ "," █ ","▀▀▀"],'2':["▀▀█","█▀▀","▀▀▀"],'3':["▀▀█","▀▀█","▀▀▀"],'4':["█ █","▀▀█","  ▀"],'5':["█▀▀","▀▀█","▀▀▀"],'6':["█▀▀","█▀█","▀▀▀"],'7':["▀▀█","  █","  ▀"],'8':["█▀█","█▀█","▀▀▀"],'9':["█▀█","▀▀█","▀▀▀"],' ':["  ","  ","  "]}
PORTS={20:"FTP-data",21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",123:"NTP",143:"IMAP",161:"SNMP",389:"LDAP",443:"HTTPS",445:"SMB",587:"SMTP-sub",636:"LDAPS",993:"IMAPS",995:"POP3S",1433:"MSSQL",3306:"MySQL",3389:"RDP",5432:"PostgreSQL",5900:"VNC",6379:"Redis",8080:"HTTP-alt",8443:"HTTPS-alt",9200:"Elasticsearch",27017:"MongoDB"}
COMMON=["123456","password","123456789","qwerty","111111","12345678","abc123","password1","admin","letmein","welcome","iloveyou","000000","dragon","shadow"]

def p(s="",c=""): print((c+str(s)+N) if c else str(s))

def figlet(t):
    t=t.upper(); rows=["","",""]
    for ch in t:
        g=FONT.get(ch,FONT[' '])
        for i in range(3): rows[i]+=g[i]+" "
    return "\n".join(rows)

def real(cmd, args):
    """Ejecuta una herramienta real del sistema si está instalada."""
    if shutil.which(cmd) is None:
        p("%s no está instalado en este sistema (instálalo con el gestor de paquetes)" % cmd, Y); return
    try:
        r=subprocess.run([cmd]+args, capture_output=True, text=True, timeout=60)
        sys.stdout.write(r.stdout); sys.stdout.write(r.stderr)
    except subprocess.TimeoutExpired:
        p("(timeout)", Y)
    except Exception as e:
        p(str(e), R)

CMDS={}
def cmd(name):
    def deco(f): CMDS[name]=f; return f
    return deco

@cmd("help")
def _help(a):
    cats={
     "sistema":["help","clear","exit","neofetch","whoami","uname","date","banner","figlet"],
     "texto/cripto":["hash","b64","hex","unhex","bin","rot13","caesar","atbash","vigenere","xor","morse","uuid","genpass"],
     "seguridad":["cidr","jwt","strength","entropy","portref","ports","crack"],
     "red (real si está instalada)":["ping","dig","whois","nmap","traceroute","ip"],
     "sistema real":["sh / ! (ejecuta un comando real del sistema)"],
    }
    p("NXT27 · edición CLI — %d comandos" % (len(CMDS)+1), VB)
    for k,v in cats.items():
        p(""); p("▸ "+k, V); p("  "+"  ".join(v), D)
    p(""); p("Pipe-friendly no, pero: hash sha256 hola · cidr 10.0.0.0/24 · ping 1.1.1.1 · !ls -la", D)

@cmd("clear")
def _clear(a): os.system("clear")
@cmd("neofetch")
def _neo(a):
    info=[(USER+"@"+HOST,""),("os",platform.platform()),("python",platform.python_version()),("cpu",str(os.cpu_count())+" nucleos"),("arch",platform.machine()),("shell",os.environ.get("SHELL","?"))]
    logo=BANNER.split("\n")[1:]
    for i in range(max(len(logo),len(info))):
        l=(logo[i] if i<len(logo) else "")
        r=""
        if i<len(info):
            r = (VB+info[i][0]+N) if info[i][1]=="" else (V+info[i][0]+N+" "+info[i][1])
        print(l+"   "+r)
@cmd("whoami")
def _who(a): p(USER)
@cmd("uname")
def _un(a): p(platform.platform())
@cmd("date")
def _date(a): p(time.strftime("%a %d %b %Y %H:%M:%S"))
@cmd("banner")
def _ban(a): p(figlet(" ".join(a) or "NXT27"), VB)
@cmd("figlet")
def _fig(a): p(figlet(" ".join(a) or "NXT27"), VB)

@cmd("hash")
def _hash(a):
    algo="sha256"; rest=a
    if a and a[0] in ("md5","sha1","sha256","sha384","sha512"): algo=a[0]; rest=a[1:]
    s=" ".join(rest).encode()
    p(hashlib.new(algo, s).hexdigest(), G)
@cmd("b64")
def _b64(a):
    if a and a[0]=="-d":
        try: p(base64.b64decode(" ".join(a[1:])).decode(errors="replace"))
        except Exception: p("base64 invalido", R)
    else: p(base64.b64encode(" ".join(a).encode()).decode())
@cmd("hex")
def _hex(a): p(binascii.hexlify(" ".join(a).encode()).decode())
@cmd("unhex")
def _unhex(a):
    try: p(binascii.unhexlify("".join(a).replace(" ","")).decode(errors="replace"))
    except Exception: p("hex invalido", R)
@cmd("bin")
def _bin(a): p(" ".join(format(b,"08b") for b in " ".join(a).encode()))
@cmd("rot13")
def _rot(a):
    import codecs; p(codecs.encode(" ".join(a),"rot13"))
@cmd("caesar")
def _caesar(a):
    try: n=int(a[0])%26
    except Exception: p("uso: caesar <n> <texto>", Y); return
    out=""
    for c in " ".join(a[1:]):
        if c.isalpha():
            base=65 if c.isupper() else 97
            out+=chr((ord(c)-base+n)%26+base)
        else: out+=c
    p(out)
@cmd("atbash")
def _atb(a):
    out=""
    for c in " ".join(a):
        if c.isalpha():
            base=65 if c.isupper() else 97
            out+=chr(base+25-(ord(c)-base))
        else: out+=c
    p(out)
@cmd("vigenere")
def _vig(a):
    if len(a)<2: p("uso: vigenere <clave> <texto>", Y); return
    key=[c for c in a[0].lower() if c.isalpha()] or ["k"]; ki=0; out=""
    for c in " ".join(a[1:]):
        if c.isalpha():
            base=65 if c.isupper() else 97
            k=ord(key[ki%len(key)])-97; ki+=1
            out+=chr((ord(c)-base+k)%26+base)
        else: out+=c
    p(out)
@cmd("xor")
def _xor(a):
    if len(a)<2: p("uso: xor <clave> <texto>", Y); return
    key=a[0].encode(); s=" ".join(a[1:]).encode()
    p("".join("%02x"%(b^key[i%len(key)]) for i,b in enumerate(s)))
@cmd("morse")
def _morse(a):
    M={'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',' ':'/'}
    p(" ".join(M.get(c,"") for c in " ".join(a).upper()))
@cmd("uuid")
def _uuid(a): p(str(uuid.uuid4()))
@cmd("genpass")
def _gen(a):
    try: n=min(int(a[0]),128)
    except Exception: n=16
    alpha="ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%&*?"
    p("".join(secrets.choice(alpha) for _ in range(n)), G)

@cmd("cidr")
def _cidr(a):
    try: net=ipaddress.ip_network(a[0], strict=False)
    except Exception: p("uso: cidr 192.168.1.0/24", Y); return
    hosts=net.num_addresses-2 if net.num_addresses>2 else net.num_addresses
    p("red:        %s" % net.with_prefixlen)
    p("mascara:    %s" % net.netmask)
    p("wildcard:   %s" % net.hostmask)
    if net.num_addresses>2:
        p("broadcast:  %s" % net.broadcast_address)
        hs=list(net.hosts())
        p("rango host: %s - %s" % (hs[0], hs[-1]))
    p("hosts:      %d" % max(0,hosts))
@cmd("jwt")
def _jwt(a):
    parts=(a[0] if a else "").split(".")
    if len(parts)<2: p("uso: jwt <token>", Y); return
    def dec(s):
        s+="="*(-len(s)%4)
        try: return json.dumps(json.loads(base64.urlsafe_b64decode(s)), indent=2, ensure_ascii=False)
        except Exception: return "(parte invalida)"
    p("HEADER:", V); p(dec(parts[0])); p("PAYLOAD:", V); p(dec(parts[1])); p("firma NO verificada", D)
@cmd("strength")
def _str(a):
    pw=" ".join(a)
    if not pw: p("uso: strength <contraseña>", Y); return
    pool=0
    if any(c.islower() for c in pw): pool+=26
    if any(c.isupper() for c in pw): pool+=26
    if any(c.isdigit() for c in pw): pool+=10
    if any(not c.isalnum() for c in pw): pool+=33
    bits=int(len(pw)*math.log2(pool or 1))
    lvl = "debil" if bits<40 else "media" if bits<60 else "fuerte" if bits<80 else "muy fuerte"
    p("longitud %d · entropia ~%d bits · %s" % (len(pw),bits,lvl), G if bits>=60 else Y)
    if pw.lower() in COMMON: p("esta en la lista de contraseñas mas comunes", R)
@cmd("entropy")
def _ent(a):
    s=" ".join(a)
    if not s: p("0"); return
    from collections import Counter
    H=-sum((c/len(s))*math.log2(c/len(s)) for c in Counter(s).values())
    p("entropia: %.3f bits/caracter (%.1f bits)" % (H, H*len(s)))
@cmd("portref")
def _pr(a):
    if not a: p("uso: portref 443 | portref ssh", Y); return
    q=a[0]
    if q.isdigit():
        p(("puerto %s -> %s"%(q,PORTS[int(q)])) if int(q) in PORTS else "puerto %s: sin referencia"%q)
    else:
        hits=[(k,v) for k,v in PORTS.items() if q.lower() in v.lower()]
        p("\n".join("%d -> %s"%(k,v) for k,v in hits) or "sin coincidencias")
@cmd("ports")
def _ports(a):
    for k in sorted(PORTS): p("%6d  %s"%(k,PORTS[k]))
@cmd("crack")
def _crack(a):
    h=(a[0] if a else "").lower()
    if len(h)!=64: p("uso: crack <hash sha256> (prueba: hash sha256 123456)", Y); return
    for pw in COMMON:
        if hashlib.sha256(pw.encode()).hexdigest()==h:
            p("encontrada: %s" % pw, G); p("-> por eso no uses contraseñas comunes", D); return
    p("no esta entre las comunes (bien)", G)

@cmd("ping")
def _ping(a):
    host=a[0] if a else "1.1.1.1"
    real("ping", (["-n","4"] if os.name=="nt" else ["-c","4"])+[host])
@cmd("dig")
def _dig(a): real("dig", a or ["github.com"])
@cmd("whois")
def _whois(a): real("whois", a or ["github.com"])
@cmd("nmap")
def _nmap(a):
    if not a: p("uso: nmap <host>  ·  usa solo contra sistemas AUTORIZADOS", Y); return
    real("nmap", a)
@cmd("traceroute")
def _tr(a): real("traceroute" if os.name!="nt" else "tracert", a or ["github.com"])
@cmd("ip")
def _ip(a): real("ip", a or ["addr"])

def dispatch(line):
    line=line.strip()
    if not line: return True
    if line in ("exit","quit"): return False
    if line.startswith("!") or line.split()[0]=="sh":
        c = line[1:].strip() if line.startswith("!") else line[2:].strip()
        if c: os.system(c)
        return True
    parts=line.split()
    name=parts[0].lower(); args=parts[1:]
    f=CMDS.get(name)
    if f:
        try: f(args)
        except Exception as e: p("error: %s"%e, R)
    else:
        p("%s: comando no encontrado — escribe 'help' (o !%s para ejecutarlo real)"%(name,line), R)
    return True

def main():
    print(BANNER)
    p("Neural eXecution Terminal · CLI // pentest — escribe 'help'  (exit para salir)", D)
    p("Prefijo ! o 'sh' para ejecutar comandos REALES del sistema (ej: !ls -la)", D)
    print()
    while True:
        try:
            line=input(V+USER+"@"+HOST+N+":"+C+"~"+N+"$ ")
        except (EOFError,KeyboardInterrupt):
            print(); break
        try:
            if not dispatch(line): break
        except Exception as e:
            p("error: %s"%e, R)
    p("hasta luego 👋", VB)

if __name__=="__main__":
    main()
