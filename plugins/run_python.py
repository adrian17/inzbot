from plugin_base import *

from pathlib import Path
import subprocess
import shutil

class PythonPlugin(Plugin):

	memory_limit_mb = 50 * (1024 * 1024)

	def __init__(self):
		super().__init__()
		self.init_chroot()

	def init_chroot(self):
		chroot = Path('chroot')
		shutil.rmtree(str(chroot), ignore_errors=True)
		chroot.mkdir()
		dev = chroot / 'dev'
		etc = chroot / 'etc'
		dev.mkdir()
		etc.mkdir()
		(dev/'random').open("w").write('0')
		(etc/'group').open("w").write('nogroup:x:65534:')
		(etc/'passwd').open("w").write('nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin')
		self.chroot_dir = chroot

	def run_python(self, nsjail_path, text):
		cmd = [
			nsjail_path,
			'-Mo',
			'--chroot', str(self.chroot_dir.resolve()),
			'-E', 'LANG=en_US.UTF-8',
			'-R/usr/bin/python3', '-R/usr/lib', '-R/lib/x86_64-linux-gnu', '-R/lib64',
			'--user', 'nobody',
			'--group', 'nogroup',
			'--time_limit', '2',
			'--disable_proc', '--iface_no_lo',
			'--cgroup_mem_max', str(self.memory_limit_mb),
			'--quiet',
			'--',
			'/usr/bin/python3', '-ISqi'
		]

		python = subprocess.Popen(cmd,
			stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			universal_newlines=True
		)
		stdout, stderr = python.communicate(text + '\n')
		return python.returncode, stdout, stderr

	@command("python", "py")
	def python3(self, bot, event):
		if not bot.nsjail_path:
			return
		returncode, stdout, stderr = self.run_python(bot.nsjail_path, event.text)
		if returncode == 0:
			if stderr not in ['>>> >>> \n', '>>> ... \n>>> \n']:
				try:
					output = stderr.split('\n')[-3] # get exception text
				except IndexError:
					output = ''
			else:
				output = stdout.split('\n', 1)[0]
		elif returncode == 109:
			output = 'timed out or memory limit exceeded'
		else:
			output = 'unknown error'
		bot.message(output[:250])
