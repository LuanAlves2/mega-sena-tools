from utils import setup_logging, get_last_concurso
from downloader import download_and_process, download_and_process_lotofacil
from cli import run_cli

if __name__ == "__main__":
    setup_logging()
    # Update both databases on startup
    mega_path = download_and_process()
    loto_path = download_and_process_lotofacil()
    mega_last = get_last_concurso(mega_path)
    loto_last = get_last_concurso(loto_path)
    run_cli(mega_last, loto_last)
