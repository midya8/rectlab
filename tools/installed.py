import tempfile,subprocess,sys,json,pathlib
P=pathlib.Path(__file__).resolve().parents[1]
examples=json.loads((P/'examples.json').read_text());runs=forgeries=0
with tempfile.TemporaryDirectory() as tmp:
 t=pathlib.Path(tmp);v=t/'venv';subprocess.run([sys.executable,'-m','venv',str(v)],check=True);py=v/'bin/python';subprocess.run([str(py),'-m','pip','install',str(P)],check=True,stdout=subprocess.DEVNULL)
 origins=json.loads(subprocess.check_output([str(py),'-c','import rectlab,rectlab.engine,rectlab.schema,rectlab.verify,rectlab.__main__,sys,json;print(json.dumps([m.__file__ for n,m in sys.modules.items() if n=="rectlab" or n.startswith("rectlab.")]))'],cwd=t,text=True));assert len(origins)==5 and all(str(v)in f for f in origins)
 for x in examples:
  inp=t/'input.json';cert=t/'cert.json';inp.write_text(json.dumps(x['input']))
  for prefix in [[str(py),'-m','rectlab'],[str(v/'bin/rectlab')]]:
   p=subprocess.run(prefix+['solve',str(inp)],cwd=t,capture_output=True,text=True,check=True);cert.write_text(p.stdout);subprocess.run(prefix+['verify',str(cert)],cwd=t,capture_output=True,text=True,check=True);q=json.loads(p.stdout);q['cover']['count']='0';cert.write_text(json.dumps(q));assert subprocess.run(prefix+['verify',str(cert)],cwd=t,capture_output=True).returncode==2;runs+=1;forgeries+=1
print(json.dumps({'installed_module_origins':len(origins),'controls':len(examples),'entrypoints':2,'solve_verify_pairs':runs,'forgeries_rejected':forgeries}))
