import click
import json
import os
import random
import sys


ALPHABET = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
LENGTH = 5
MAX_TRIES = 1000


def real_warning(msg):
    print('Warning: ' + msg, file=sys.stderr)

warn = real_warning


def generate_string(length, alphabet):
    return ''.join(
        [random.choice(alphabet) for _ in range(length)]
    )


def generate_unique_string(existing):
    new_uid = generate_string(LENGTH, ALPHABET)
    i = 0
    while new_uid in existing:
        new_uid = generate_string(LENGTH, ALPHABET)
        i += 1
        if i > MAX_TRIES:
            raise RuntimeError(
                'Generated ID not unique within {} tries'.format(MAX_TRIES)
            )
    return new_uid


def iter_datamodel_chapter(root):
    for act_dir, dirs, files in os.walk(root):
        for name in files:
            if name.startswith('chapter') and name.endswith('.json'):
                with open(os.path.join(act_dir, name)) as f:
                    yield json.load(f)


def walk_datamodel_uids(root):
    uids = set()
    for chapter in iter_datamodel_chapter(root):
        question_n = 0
        for question in chapter['questions']:
            question_n += 1
            if 'uid' not in question:
                    warn('UID not set in {}:{}:{}'.format(
                        chapter['namespace'],
                        chapter['chapterid'],
                        question_n
                    ))
            elif question['uid'] in uids:
                warn('UID not unique in {}:{}:{}'.format(
                    chapter['namespace'],
                    chapter['chapterid'],
                    question_n
                ))
            else:
                uids.add(question['uid'])
            answer_n = 0
            for answer in question.get('answers', []):
                    if 'uid' not in answer:
                        warn('UID not set in {}:{}:{}:{}'.format(
                            chapter['namespace'],
                            chapter['chapterid'],
                            question_n,
                            answer_n
                        ))
                    elif answer['uid'] in uids:
                        warn('UID not unique in {}:{}:{}:{}'.format(
                            chapter['namespace'],
                            chapter['chapterid'],
                            question_n,
                            answer_n
                        ))
                    else:
                        uids.add(answer['uid'])
    return uids


@click.group()
@click.argument('dskm-root', type=click.Path())
@click.option('-q', '--quiet', is_flag=True)
@click.version_option(version='0.1', prog_name='DS KM UID generator')
@click.pass_context
def cli(ctx, dskm_root, quiet):
    ctx.obj['root'] = dskm_root
    if quiet:
        global warn
        warn = lambda msg: None


@cli.command()
@click.option('-n', '--count', default=1, type=int)
@click.option('-j', '--json-line', is_flag=True)
@click.pass_context
def generate(ctx, count, json_line):
    root = ctx.obj['root']
    uids = walk_datamodel_uids(root)

    print_uid = lambda uid: print(uid)
    if json_line:
        print_uid = lambda uid: print('"uid": "{}",'.format(uid))

    for i in range(count):
        x = generate_unique_string(uids)
        uids.add(x)
        print_uid(x)


@cli.command()
@click.pass_context
def list(ctx):
    root = ctx.obj['root']
    uids = walk_datamodel_uids(root)
    for uid in uids:
        print(uid)


if __name__ == '__main__':
    cli(obj={})
