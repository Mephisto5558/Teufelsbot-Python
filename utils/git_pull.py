from asyncio import subprocess, create_subprocess_exec

from .logger import log


async def git_pull():
  process = await create_subprocess_exec('git pull', text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = await process.communicate()

  if process.returncode:
    log.error('Exec error: %s', stderr)
    return stderr

  if stdout: log.info('OUT: %s', stdout.decode(encoding='utf8').strip())
  if stderr: log.info('ERR: %s', stderr.decode(encoding='utf8').strip())

  return 'OK'
