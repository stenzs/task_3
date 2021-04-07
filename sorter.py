import click
from mp3_tagger import MP3File, VERSION_1
import os
import shutil
@click.command()
@click.option('-s', '--src-dir', default=os.getcwd(), help='Исходная директория, по умолчанию "."')
@click.option('-d', '--dst-dir', default=os.getcwd(), help='Целевая директория, по умолчанию "."')
def main(src_dir, dst_dir):
    '''
    Программа для сортировки mp3 файлов.

    Если в пути до директории пирсутствуют пробелы, используйте двойные кавычки:

    Пример: -s "C:/User/Desktop/Music sort"
    '''
    folder1 = src_dir
    folder2 = dst_dir
    try:
        os.chdir(folder2)
        os.chdir(folder1)
    except BaseException:
        print('...\nОшибка в наименовании каталогов, '
              'вызовите программу снова\nДля спавки исрользуйте флаг --help.')
        raise SystemExit
    os.chdir(folder1)
    musiclist = os.listdir()
    for i in musiclist:
        if os.path.splitext(i)[1] == '.mp3':
            mp3 = MP3File(i)
            mp3.set_version(VERSION_1)
            if mp3.artist is None or len(mp3.artist.strip()) == 0:
                print('...\nОтсутствует наименование исполнителя, '
                      'либо недостаточно прав, файл не учавствует в сортировке.')
                print(folder1 + '/' + i, '-> X')
                continue
            folder_artist = mp3.artist.strip()
            patch1 = folder2 + '/' + folder_artist
            if not os.path.exists(patch1):
                try:
                    os.mkdir(patch1)
                except OSError:
                    os.chdir(folder1)
                    print('...\nНеверный синтаксис имени каталога,'
                          'либо недостаточно прав, файл не учавствует в сортировке.')
                    print(folder1 + '/' + i, '-> X')
                    continue
            os.chdir(patch1)
            if mp3.album is None or len(mp3.album.strip()) == 0:
                os.chdir(folder1)
                os.rmdir(patch1)
                print('...\nОтсутствует наименование альбома,'
                      'либо недостаточно прав, файл не учавствует в сортировке.')
                print(folder1 + '/' + i, '-> X')
                continue
            folder_album = mp3.album.strip()
            patch2 = patch1 + '/' + folder_album
            if not os.path.exists(patch2):
                try:
                    os.mkdir(patch2)
                except OSError:
                    os.chdir(folder1)
                    os.rmdir(patch1)
                    print('...\nНеверный синтаксис имени каталога,'
                          'либо недостаточно прав, файл не учавствует в сортировке.')
                    print(folder1 + '/' + i, '-> X')
                    continue
            os.chdir(patch2)
            shutil.move(folder1 + '/' + i, patch2 + '/' + i)
            i_new = i
            print('...')
            if mp3.song is not None and len(mp3.song.strip()) != 0:
                i_new = mp3.song.strip() + ' - ' + mp3.artist.strip() + ' - ' + mp3.album.strip() + '.mp3'
                try:
                    os.rename(i, i_new)
                except OSError:
                    i_new = i
                    print('Неверный синтаксис имени файла,'
                          'либо недостаточно прав, название осталось прежним.')
            else:
                print('Отсутствует наименование, '
                      'либо недостаточно прав, название осталось прежним.')
            print(folder1 + '/' + i, '->', patch2 + '/' + i_new)
            os.chdir(folder1)
    print('...\nСортировка завершена.')
if __name__ == '__main__':
    main()