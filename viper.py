#!/usr/bin/env python3

import sys, os

variables = {}
functions = {}

def text(txt):
  tx = txt.split("%")
  end = []
  for tet in tx:
    t = tet.strip()
    if t[0] == '"' and t[-1] == '"':
      end.append(t[1:-1])
    elif t[0] == "'" and t[-1] == "'":
      end.append(t[1:-1])
    elif t == "True":
      return True
    elif t == "False":
      return False
    elif t[0] == "0" or t[0] == "1" or t[0] == "2" or t[0] == "3" or t[0] == "4" or t[0] == "5" or t[0] == "6" or t[0] == "7" or t[0] == "8" or t[0] == "9":
      try:
        return int(t) 
      except: 
        return float(t)
    elif t[0] == "(" and t[-1] == ")":
      if t.find("==") != -1:
        lhs = t[1:t.find("==")].strip()
        rhs = t[t.find("==") + 2].strip()
        if text(lhs) == text(rhs):
          return True
        else:
          return False
      elif t.find("!=") != -1:
        lhs = t[:t.find("!=")].strip()
        rhs = t[t.find("!=") + 2].strip()
        if text(lhs) != text(rhs):
          return True
        else:
          return False
      elif t.find("<") != -1:
        lhs = t[:t.find("<")].strip()
        rhs = t[t.find("<") + 1:].strip()
        if float(text(lhs)) < float(text(rhs)):
          return True
        else:
          return False
      elif t.find(">") != -1:
        lhs = t[:t.find(">")].strip()
        rhs = t[t.find(">") + 1:].strip()
        if float(text(lhs)) > float(text(rhs)):
          return True
        else:
          return False
      elif t.find("<=") != -1:
        lhs = t[:t.find("<=")].strip()
        rhs = t[t.find("<=") + 2:].strip()
        if float(text(lhs)) <= float(text(rhs)):
          return True
        else:
          return False
      elif t.find(">=") != -1:
        lhs = t[:t.find(">=")].strip()
        rhs = t[t.find(">=") + 2:].strip()
        if float(text(lhs)) >= float(text(rhs)):
          return True
        else:
          return False
      else:
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
        tt.append(text(te.strip()))
      return tt
    elif t[0] == "{" and t[-1] == "}":
      tex = t[1:-1].split(",")
      tt = {}
      for te in tex:
        p1 = te[:te.find(":")].strip()
        p2 = te[te.find(":") + 1:].strip()
        tt[text(p1)] = text(p2)
      return tt
    elif t[0] != "[" and t[-1] == "]":
      var = variables[t[:t.find("[")]]
      end.append(var[text(t[t.find("[") + 1:-1])])
    elif t[:4] == "gen{" and t[-1] == "}":
      num = text(t[4:-1])
      tt = []
      for n in range(1, num):
        tt.append(n)
      tt.append(num)
      return tt
    else:
      if t in variables:
        try:
          if type(variables[t]) == list:
            return list(variables[t])
          elif type(variables[t]) == bool:
            return bool(variables[t])
          elif type(variables[t]) == int:
            return int(variables[t])
          elif type(variables[t]) == float:
            return float(variables[t])
          elif type(variables[t]) == dict:
            return dict(variables[t])
          else:
            end.append(variables[t])
        except ValueError:
          print("\033[91m The type is incorrect \033[92m")
          return ''
      else:
        print("\033[91m Variable " + txt + " does not exist \033[92m")
        return ''
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
    variables[cmd[4:cmd.find("=")].strip()] = text(cmd[cmd.find("=") + 1:-1])
  elif cmd[:6] == "input{" and cmd[-1] == "}":
    variables[cmd[6:cmd.find("=")].strip()] = input(text(cmd[cmd.find("=") + 1:-1]))
  elif cmd[:7] == "import{" and cmd[-1] == "}":
    try:
      lines = open(text(cmd[7:-1]) + ".vp")
      lines = lines.read()
      lines = lines.split("\n")
      execut(lines)
    except FileNotFoundError:
      print("\033[91m Library" + text(cmd[7:-1]) + " does not exist \033[92m")
  elif cmd in functions:
    code = functions[cmd]
    execut(code)
  elif cmd[:4] == "cmd{" and cmd[-1] == "}":
    os.system(text(cmd[4:-1]))
  elif cmd[:3] == ">>>":
    pass
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
      elif cmd[:3] == "if{" and cmd[-3:] == "}=[":
        cond = cmd[3:-3]
        code = []
        while True:
          l = l + 1
          dcmd = lines[l].lstrip()
          if dcmd == "]":
            break
          else:
            code.append(dcmd)
        if bool(text(cond)):
          execut(code)
      elif cmd[:4] == "for{" and cmd.find("}in{") and cmd[-3:] == "}=[":
        loop = cmd[4:cmd.find("}in{")]
        varb = cmd[cmd.find("}in{") + 4:-3]
        code = []
        while True:
          l = l + 1
          dcmd = lines[l].lstrip()
          if dcmd == "]":
            break
          else:
            code.append(dcmd)
        for lp in text(varb):
          variables[loop] = lp
          execut(code)
      elif cmd[:6] == "while{" and cmd.find("}in{") and cmd[-3:] == "}=[":
        cond = cmd[6:-3]
        code = []
        while True:
          l = l + 1
          dcmd = lines[l].lstrip()
          if dcmd == "]":
            break
          else:
            code.append(dcmd)
        while bool(text(cond)):
          execut(code)
      else:
        main(cmd)
      l = l + 1
    except IndexError:
      break



def viper():
  while True:
    cmd = input("\033[92m ~> \033[92m")
    if cmd[:6] == "print{" and cmd[-1] == "}":
      print(text(cmd[6:-1]))
    elif cmd[:4] == "var{" and cmd[-1] == "}":
      variables[cmd[4:cmd.find("=")].strip()] = text(cmd[cmd.find("=") + 1:-1])
    elif cmd[:6] == "input{" and cmd[-1] == "}":
      variables[cmd[6:cmd.find("=")].strip()] = input(text(cmd[cmd.find("=") + 1:-1]))
    elif cmd in functions:
      code = functions[cmd]
      execut(code)
    elif cmd[:7] == "import{" and cmd[-1] == "}":
      try:
        lines = open(text(cmd[7:-1]) + ".vp")
        lines = lines.read()
        lines = lines.split("\n")
        execut(lines)
      except FileNotFoundError:
        print("\033[91m Library " + text(cmd[7:-1]) + " does not exist \033[92m")
    elif cmd[:4] == "met{" and cmd[-3:] == "}=[":
      name = cmd[4:-3]
      code = []
      while True:
        dcmd = input("\033[92m ---) ").lstrip()
        if dcmd == "]":
          break
        else:
          code.append(dcmd)
      functions[name] = code
    elif cmd[:3] == "if{" and cmd[-3:] == "}=[":
      cond = cmd[3:-3]
      code = []
      while True:
        dcmd = input("\033[92m ---) ").lstrip()
        if dcmd == "]":
          break
        else:
          code.append(dcmd)
      if bool(text(cond)):
        execut(code)
    elif cmd[:4] == "for{" and cmd.find("}in{") and cmd[-3:] == "}=[":
      loop = cmd[4:cmd.find("}in{")]
      varb = cmd[cmd.find("}in{") + 4:-3]
      code = []
      while True:
        dcmd = input("\033[92m ---) ").lstrip()
        if dcmd == "]":
          break
        else:
          code.append(dcmd)
      for lp in text(varb):
        variables[loop] = lp
        execut(code)
    elif cmd[:6] == "while{" and cmd.find("}in{") and cmd[-3:] == "}=[":
      cond = cmd[6:-3]
      code = []
      while True:
        dcmd = input("\033[92m ---) ").lstrip()
        if dcmd == "]":
          break
        else:
          code.append(dcmd)
      while bool(text(cond)):
        execut(code)
    elif cmd[:4] == "cmd{" and cmd[-1] == "}":
      os.system(text(cmd[4:-1]))
    elif cmd[:3] == ">>>":
      pass
    elif cmd == "":
      pass
    else:
      print("\033[91m" + cmd + " is an invalid command \033[92m")

if len(sys.argv) == 2:
  lines = open(sys.argv[1])
  lines = lines.read()
  lines = lines.split("\n")
  execut(lines)
else:
  viper()