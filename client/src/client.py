import click
import requests
import json
import pprint
from populate import populate

from config import task_commands
from api import api_get, api_post
from activity_logger import log_response, log_error

pp = pprint.PrettyPrinter(indent=2, width=50)

@click.group()
def cli():
    pass

@click.command(name="get")
@click.option('-t', '--task', is_flag=True, default=True, help='Specifies the get request as tasks')
@click.option('-r', '--results', is_flag=True, help='Specifies the get request as task results')
@click.option('-i', '--info', is_flag=True, help='Specifies the get request as info')
@click.option('-ip', '--ip-address', help='Specifies target ip for the get request')
@click.option('-id', '--target-id', help='Specifies target id for the get request')
def get(task, results, info, ip_address, target_id):
    endpoint = '/tasks'
    res = {}
    
    if results:
        endpoint = '/results'
        res = api_get(endpoint)
    if info or ip_address or target_id:
        endpoint = '/targets'
        res = api_get(endpoint)
        if target_id:
            res = get_target_by_id(res, target_id)
        elif ip_address:
            res = get_target_by_ip(res, ip_address)
    else:
        res = api_get(endpoint)

    log_response(res)
    
    pp.pprint(res)

# Get Helper Functions
def get_target_by_id(data, id):
    for item in data:
        if item["target_id"] == id:
            return item

def get_target_by_ip(data, ip):
    for item in data:
        if item["ip"] == ip:
            return item

@click.command(name="add")
@click.option(
    '-t',
    '--task',
    help=f"""\
        Specifies the task to add.
        Available Tasks:
        {task_commands}
    """
)
def add(task):
    endpoint = '/tasks'
    
    task.lower()
    if task not in task_commands:
        click.echo(f"""The task you attempted to add was {task}.\nThis is not a valid task. Please try one of the following:\n{task_commands}
        """)
        click.echo("No tasks have been added. Please try again.")
        return
    
    proceed = None
    if task == 'encrypt':
        print("WARNING: This task will execute encryption on the target(s).")
        print("Please confirm: (y/n)")
        proceed = input().lower()
    elif task == 'decrypt':
        print("WARNING: This task will execute decryption on the target(s).")
        # print("Please confirm: (y/n) ", end=" ")
        proceed = input("Please confirm: (y/n)").lower()
        
    if proceed != 'y' and proceed is not None:
        print("EXITING...")
        return
    
    payload = {
        "task_type": task
    }
    try:
        res = api_post(endpoint, payload)
        pp.pprint(res)
        log_response(res)
    except Exception as e:
        log_error(e)
    



cli.add_command(get)
cli.add_command(add)

#! TODO: TESTING ONLY
populate()

if __name__ == "__main__":
    cli()