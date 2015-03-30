import os.path
from fabric.api import task,env,run,local
from fabric.operations import put
from fabric.context_managers import cd,lcd

env.hosts = ['billmerrill@web481.webfaction.com']
env.forward_agent = True

deploy_root = '/home/billmerrill/releases/vcs'
topo_root = '%s/topophile' % deploy_root
backup_root = '/home/billmerrill/deploy-backup'

apps = {'dotcom': { 'root':'/home/billmerrill/webapps/topophile_com',
                    'git_files': 'gaua/topophile.com'},
        'ebeko': {'root': '/home/billmerrill/webapps/ebeko',
                  'git_files': 'ebeko/ebeko'},
        'bam': {'root': '/home/billmerrill/webapps/scotch_wsgi',
                'restart': '/home/billmerrill/webapps/scotch_wsgi/apache2/bin/restart'} }


@task
def uptime():
  run('uptime')

  
def name_release_dir():
    return 'topophile-%s' % datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    
@task 
def deploy_gone_fishing():
    put('/Users/bill/topo/gaua/gone_fishing/*', 
        '/home/billmerrill/webapps/topophile_gone_fishing')


def pre_deploy():
    exists = run('test -d %s; echo $?' % deploy_root) == '0'
    if not exists:
        run('mkdir -p %s' % deploy_root)
        
        with cd(deploy_root):
            run('git clone git@github.com:billmerrill/topophile.git')
    
        
def get_version(tag=None):
    with cd(topo_root):
        run('git checkout master')
        run('git pull')
        if tag:
            run('git checkout tags/%s' % tag)   


def file_exists(name):
    return run('test -e %s; echo $?' % name, quiet=True) == '0'

    
def cycle_backup(app):
    '''
    make a copy of the running files before deploying an app
    '''
    app_backup_path = '%s/%s' % (backup_root, app)
    print 'app backup path %s ' % app_backup_path
    if file_exists(app_backup_path):
        run('rsync -a %s/ %s.old/' % (app_backup_path, app_backup_path))
    
    # cp running app to backup
    run('rsync -a %s/ %s/' % (apps[app]['root'], app_backup_path))
    

def deploy_static_app(app):
    cycle_backup(app)
  
    app_dir = apps[app]['root']
    
    # sanity check before nuking
    if len(app_dir) > 20:
        with cd(app_dir):
            print 'XXX rm -rf start'
            
    with cd(topo_root):
        run('cp -r %s/* %s/' % (apps[app]['git_files'], apps[app]['root']))
    
def restart_wsgi_app(app):
    cmd = apps[app]['restart']
    if len(cmd) > 20:
        run(cmd)

@task
def deploy_all(tag=None, static_only=False):
    '''
    deploy topophile.com, ebeko, and bam
    
    1. checkout
    2. copy ebeko
    3. copy topophile.com
    4. restart bam
    '''
    pre_deploy()
    get_version(tag)
    deploy_static_app('dotcom')
    deploy_static_app('ebeko')
    restart_wsgi_app('bam')

@task
def deploy_static(tag=None):
    deploy_all(tag, static_only=True)

@task
def deploy_bam(tag=None):
    pre_deploy()
    get_version(tag)
    restart_wsgi_app('bam')