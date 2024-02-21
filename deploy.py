import ghp_import


def deploy():
  ghp_import.ghp_import('-n', 'public', 'gh-pages')
