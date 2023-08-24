from subprocess import CalledProcessError, run


def git_pull():
  try:
    data = run('git pull', capture_output=True, text=True, check=True, shell=True)
  except CalledProcessError as err:
    print(f'GIT PULL\nExec error: {err}')
    return err

  print(
      'GIT PULL\n' +
      (f'out: {data.stdout.strip()}\n' if data.stdout else '') +
      (f'err: {data.stderr.strip()}\n' if data.stderr else '')
  )

  return 'OK'
