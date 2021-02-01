#!/usr/bin/env python3

import sys

variables = {}
functions = {}

def text(txt):
  tx = txt.split("%")
  end = []
  for t in tx:
    if t[0] == '"' and t[-1] == '"':
      end.append(t[1:-1])
    elif t[0] == "'" and t[-1] == "'":
      end.append(t[1:-1])
    elif t[0] == "0" or t[0] == "1" or t[0] == "2" or t[0] == "3" or t[0] == "4" or t[0] == "5" or t[0] == "6" or t[0] == "7" or t[0] == "8" or t[0] == "9":
      try:
        return int(t) 
      except: 
        return float(t)
    elif t[0] == "(" and t[-1] == ")":
      _expr = txt[1:-1]
      for _sign in ["-", "+", "*", "/", "%", "^"]:
        index = _expr.find( _sign)
        if index > 0:
          lhs = _expr[:index].strip()
          rhs = _expr[index + 1:].strip()
          if _sign == '/':
            return int(text(lhs))/int(text(rhs))
          elif _sign == '*':
            return int(text(lhs))*int(text(rhs))
          elif _sign == '+':
              return int(text(lhs))+int(text(rhs))
          elif _sign == '-':
            return int(text(lhs))-int(text(rhs))
          elif _sign == '#':
            return int(text(lhs))%int(text(rhs))
          elif _sign == '^':
            return int(text(lhs))**int(text(rhs))
    elif t[0] == "[" and t[-1] == "]":
      tex = t[1:-1].split(",")
      tt = []
      for te in tex:
        tt.append(text(te))
      return tt
    elif t[0] != "[" and t[-1] == "]":
      var = variables[t[:t.find("[")]]
      end.append(var[int(t[t.find("[") + 1:-1])])
    else:
      try:
        end.append(str(variables[t]))
      except ValueError:
        print("\033[91m The type is incorrect \033[92m")
        return ''
      except KeyError:
        print("\033[91m Variable " + txt + " does not exist \033[92m")
        return ''
      except TypeError:
        end.append(variables[t])
  try:
    end = "".join(tuple(end))
  except:
    en = []
    for e in end:
      en.append(str(e))
    end = "".join(tuple(end))
  try:
    return end
  except TypeError:
    return str(end)

def main(cmd):
  if cmd[:6] == "print{" and cmd[-1] == "}":
    print(text(cmd[6:-1]))
  elif cmd[:4] == "var{" and cmd[-1] == "}":
    variables[cmd[4:cmd.find("=")]] = text(cmd[cmd.find("=") + 1:-1])
  elif cmd[:6] == "input{" and cmd[-1] == "}":
    variables[cmd[6:cmd.find("=")]] = input(text(cmd[cmd.find("=") + 1:-1]))
  elif cmd in functions:
    code = functions[cmd]
    for line in code:
        main(line)
  elif cmd == "":
    pass
  else:
    print("\033[91m" + cmd + " is an invalid command \033[92m")
  

def execut(lines):
  l = 0
  for ln in range(len(lines)):
    try:
      cmd = lines[l]
      if cmd[:4] == "met{" and cmd[-3:] == "}=[":
        name = cmd[4:-3]
        code = []
        while True:
          l = l + 1
          dcmd = lines[l].lstrip()
          if dcmd == "]":
            break
          else:
            code.append(dcmd)
        functions[name] = code
      else:
        main(cmd)
      l = l + 1
    except IndexError:
      break

if len(sys.argv) == 2:
  lines = open(sys.argv[1])
  lines = lines.read()
  lines = lines.split("\n")
else:
  lines = []
  while True:
    cmd = input("\033[92m ~> ")
    if cmd == "run{}":
      break
    else:
      lines.append(cmd)
  execut(lines)