import pathlib

from dotenv import load_dotenv
cwd = pathlib.Path(__file__).parent.absolute()

load_dotenv(f'{cwd}/.test_env',verbose=True)
