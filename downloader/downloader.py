from datetime import datetime
import requests


def get_from_push_shift(subreddit, after, before):
    all_data = make_call(subreddit=subreddit, after=after, before=before)
    max_created = get_max_created(all_data)
    ids = []
    for item in all_data:
        ids.append(item['id'])
    duplicating = False
    while not duplicating:
        new_data = make_call(subreddit=subreddit, after=max_created, before=before)
        max_created = get_max_created(new_data)
        if len(new_data) < 1 or max_created == 0:
            duplicating = True
            continue
        for item in new_data:
            item_id = item['id']
            if item_id not in ids:
                ids.append(item_id)
                all_data.append(item)
            else:
                duplicating = True
    return all_data, ids


def get_max_created(data):
    max_created = 0
    for item in data:
        created_utc = item['created_utc']
        if created_utc > max_created:
            max_created = created_utc
    return max_created


def make_call(subreddit, after, before):
    base_url = "https://api.pushshift.io/reddit/search/submission/"
    query_string = {
        "subreddit": subreddit,
        "sort": "asc",
        "sort_type": "created_utc",
        "after": int(after),
        "before": int(before),
        "size": 1000
    }
    res = requests.get(url=base_url, params=query_string)
    if res.status_code != 200:
        print(f"There was an error with status code {res.status_code}")
        print(f"Error text: '{res.text}'")
        return []
    return res.json()['data']


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser(description='''A tool to pull all subreddit submissions over a 
     specified date range, using the pushshift.io api''')
    parser.add_argument('-s', '--subreddit',
                        required=False,
                        help='Specify the subreddit from which to fetch submissions',
                        dest='subreddit',
                        default="dailyprogrammer")
    parser.add_argument('-a', '--after',
                        required=False,
                        help='''Specify the unix epoch timestamp that all submissions should occur after. The default
                        is January 1st around midnight (1131160788)''',
                        dest='after',
                        type=int,
                        default=1131160788)
    parser.add_argument('-b', '--before',
                        required=False,
                        help=f'''Specify the unix epoch timestamp that all submissions should occur before. The default
                        before value is the time of execution. E.g. if we ran now the unix epoch time used 
                        would be {int(datetime.now().timestamp())}''',
                        dest='before',
                        type=int,
                        default=int(datetime.now().timestamp()))
    parser.add_argument('-f', '--f',
                        required=False,
                        help='Specify an output file',
                        dest='filename',
                        default='submissions.json')
    args = parser.parse_args()
    data, ids = get_from_push_shift(subreddit=args.subreddit, after=args.after, before=args.before)
    with open(args.filename, 'w', newline='') as outfile:
        outfile.write(json.dumps(data))
    print(f"wrote {len(ids)} posts to {args.filename}")


if __name__ == '__main__':
    main()
