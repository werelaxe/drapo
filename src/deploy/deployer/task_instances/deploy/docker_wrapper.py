from subprocess import run, PIPE, CompletedProcess


class CommandExecutionError(Exception):
    pass


def create_message(cp: CompletedProcess):
    return f"status_code={cp.returncode}, stdout={cp.stdout.read()}, stderr={cp.stderr.read()}"


def check_process_state(cp: CompletedProcess):
    if cp.returncode:
        raise CommandExecutionError(f"Unsuccessful executing command {cp.args}, message={create_message(cp)}")


def docker_stack_deploy(compose_file_path, name):
    r = run(f"docker stack deploy --compose-file {compose_file_path} {name}", shell=True, stdout=PIPE, stderr=PIPE)
    check_process_state(r)


def docker_stack_rm(name):
    r = run(f"docker stack rm {name}", shell=True, stdout=PIPE, stderr=PIPE)
    check_process_state(r)
