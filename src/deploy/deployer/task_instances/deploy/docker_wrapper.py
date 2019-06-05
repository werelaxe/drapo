from subprocess import run


def docker_stack_deploy(compose_file_path, name):
    r = run(f"docker stack deploy --compose-file {compose_file_path} {name}", shell=True)
    print(r)
