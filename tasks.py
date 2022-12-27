from invoke import task
import keyring


@task
def poetry_setup(c):
    #resp = c.run("poetry config repositories.gitea.url", hide=True, warn=True)
    #if resp.ok:
    #    return
    # poetry should know to pull from our local gitea server
    c.run(
        "poetry source add gitea 'http://sinus.smurfless.com:3000/api/packages/smurfless1/pypi/simple'"
    )
    # now teach it to publish to our local gitea server
    c.run(
        "poetry config repositories.gitea 'http://sinus.smurfless.com:3000/api/packages/smurfless1/pypi'"
    )
    # poetry lies about whether the key is set, so always set it
    api_key = keyring.get_password('gitea API key', 'smurfless1')
    c.run(f"poetry config pypi-token.gitea {api_key}")


@task
def poetry_unset(c):
    c.run("poetry config repositories.gitea.url --unset ")
    c.run("poetry config repositories.gitea --unset")
    c.run("poetry config pypi-token.gitea --unset")


@task
def black(c):
    c.run("black onepassword_keyring/*.py tests/*.py")


@task
def setup_py(c):
    c.run("poetry2setup > setup.py")


@task(black, setup_py)
def build(c):
    c.run("poetry build")


@task(build)
def publish(c):
    c.run(f"poetry publish --repository gitea")
