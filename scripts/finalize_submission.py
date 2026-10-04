from pathlib import Path
import os, shutil, subprocess, sys

root = Path(__file__).resolve().parents[1]
os.chdir(root)
python = root/'aipdd_env/Scripts/python.exe'
git = shutil.which('git') or next((str(p) for p in [root/'tools/mingit/cmd/git.exe', root.parent/'.tools/mingit/cmd/git.exe', Path(os.environ['LOCALAPPDATA'])/'Programs/Git/cmd/git.exe', Path('C:/Program Files/Git/cmd/git.exe')] if p.exists()), 'git')
def run(*args):
    subprocess.run(list(map(str,args)), check=True)
def capture(*args):
    return subprocess.check_output(list(map(str,args)), text=True, encoding='utf-8')
def save(name, text):
    (root/name).write_text(text, encoding='utf-8')
if not python.exists():
    run(sys.executable,'-m','venv','aipdd_env')
run(python,'-m','pip','install','-r','requirements.txt')
run(python,'-m','ipykernel','install','--user','--name','aipdd_env','--display-name','Python (aipdd_env)')
frozen = capture(python,'-m','pip','freeze')
save('requirements.txt',frozen)
save('requirements-lock.txt',frozen)
if not (root/'.git').exists():
    run(git,'init','-b','main')
    run(git,'config','user.name','Noor ul Huda')
    run(git,'config','user.email',os.environ.get('LAB_GIT_EMAIL','noor-ul-huda@example.invalid'))
    run(git,'add','.gitignore','scripts','data','models','src','configs','logs','README.md','SUBMISSION_CHECKLIST.md')
    run(git,'commit','-m','Initial project structure and gitignore')
    run(git,'checkout','-b','feature/lab01-setup')
    run(git,'add','requirements.txt','requirements.in','requirements-lock.txt')
    run(git,'commit','-m','Add pinned lab dependencies')
    run(git,'checkout','main')
    run(git,'merge','--no-ff','feature/lab01-setup','-m','Merge feature/lab01-setup')
notebook = 'notebooks/Lab01_Foundations_AI_Engineering.ipynb'
run(python,'-m','jupyter','nbconvert','--to','notebook','--execute','--inplace',notebook,'--ExecutePreprocessor.kernel_name=aipdd_env','--ExecutePreprocessor.timeout=300')
run(python,'-m','jupyter','nbconvert','--to','html',notebook)
save('evidence/package_verification.txt',capture(python,'-c',"import sys,numpy,cv2,torch,matplotlib,ultralytics; print('Student: Noor ul Huda'); print('Python:',sys.version); print('Environment:',sys.prefix); print('numpy:',numpy.__version__); print('cv2:',cv2.__version__); print('torch:',torch.__version__); print('matplotlib:',matplotlib.__version__); print('ultralytics:',ultralytics.__version__)"))
lines = ['Noor_ul_Huda_LAB01/']
for current, dirs, files in os.walk(root):
    dirs[:] = sorted(d for d in dirs if d not in {'.git','aipdd_env','__pycache__','.ipynb_checkpoints'})
    for name in sorted(dirs+files):
        lines.append('  '*len(Path(current).relative_to(root).parts)+'|-- '+name+('/' if name in dirs else ''))
save('evidence/tree_final.txt','\n'.join(lines)+'\n')
save('evidence/git_log_oneline.txt',capture(git,'log','--oneline','--graph','--decorate','--all'))
save('evidence/git_branches.txt',capture(git,'branch','-vv'))
run(git,'add','.')
run(git,'commit','-m','Add executed Noor ul Huda notebook and local lab evidence')
save('evidence/git_status.txt',capture(git,'status'))
save('evidence/git_status_short.txt',capture(git,'status','--short'))
run(git,'add','evidence')
run(git,'commit','-m','Record final Git status evidence')
run(git,'status','--short')
print('Lab complete. Git email is a placeholder unless LAB_GIT_EMAIL was supplied.')
