"""Reusable template: navigate a Feishu wiki to find a document by title.
Usage: modify DOC_TOKEN and SEARCH_TITLE, then run with python3.
"""
import subprocess, json, os, sys

# === CONFIGURE THESE ===
DOC_TOKEN = 'PLC2wV49MiR9Nnkoc00clIUanG5'  # Starting wiki/doc token
SEARCH_TITLE = '画板'  # Title substring to search for
# =======================

def feishu_get(path):
    """Authenticated GET to Feishu open API."""
    r = subprocess.run(['curl', '-s', '-X', 'POST',
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({'app_id': os.environ['FEISHU_APP_ID'],
                          'app_secret': os.environ['FEISHU_APP_SECRET']})],
        capture_output=True, text=True)
    token = json.loads(r.stdout)['tenant_access_token']
    auth = 'Bearer ' + token
    r = subprocess.run(['curl', '-s',
        'https://open.feishu.cn/open-apis' + path,
        '-H', 'Authorization: ' + auth],
        capture_output=True, text=True)
    return json.loads(r.stdout)

# Step 1: Get node info
print('=== Step 1: Node info ===')
ni = feishu_get('/wiki/v2/spaces/get_node?token=' + DOC_TOKEN)
node = ni['data']['node']
print('type=%s title=%s has_child=%s space=%s' % (
    node['obj_type'], node.get('title',''), node.get('has_child'), node['space_id']))

# Step 2: Get document blocks to find sub-pages and embedded content
print('\n=== Step 2: Document blocks ===')
blocks = feishu_get('/docx/v1/documents/' + DOC_TOKEN + '/blocks?page_size=100')
items = blocks.get('data', {}).get('items', [])
print('Total blocks: %d' % len(items))

found = None
for b in items:
    bt = b.get('block_type', '?')
    bid = b.get('block_id', '?')

    # Check page title
    page = b.get('page', {})
    text_elems = page.get('elements', [])
    text = ''.join(e.get('text_run', {}).get('content', '') for e in text_elems)
    if text:
        print('[%d] PAGE: "%s"  children=%s' % (bt, text, b.get('children', [])))

    # Check heading text
    heading = b.get('heading2', {}) or b.get('heading1', {}) or b.get('heading3', {})
    htext = ''.join(e.get('text_run', {}).get('content', '') for e in heading.get('elements', []))
    if htext:
        print('[%d] HEADING: "%s"' % (bt, htext))

    # Check bullet text
    bullet = b.get('bullet', {})
    btext = ''.join(e.get('text_run', {}).get('content', '') for e in bullet.get('elements', []))
    if btext:
        print('[%d] BULLET: "%s"' % (bt, btext))

    # Check embedded content
    if bt == 43:  # Board
        board_token = b.get('board', {}).get('token', '')
        print('[%d] BOARD: token=%s' % (bt, board_token))

    if bt == 51:  # Sub-page list
        print('[%d] SUB_PAGE_LIST: wiki_token=%s' % (bt, b.get('sub_page_list', {}).get('wiki_token', '')))

    # Check for children (sub-blocks)
    children = b.get('children', [])
    for child_id in children:
        # Read child block detail
        child = feishu_get('/docx/v1/documents/' + DOC_TOKEN + '/blocks/' + child_id)
        cb = child.get('data', {}).get('block', {})
        ct = cb.get('block_type', '?')
        ctext = ''.join(
            e.get('text_run', {}).get('content', '')
            for elem_list in [cb.get('text', {}).get('elements', []),
                              cb.get('heading1', {}).get('elements', []),
                              cb.get('heading2', {}).get('elements', []),
                              cb.get('bullet', {}).get('elements', [])]
            for e in elem_list
        )
        print('  child [%d] %s: "%s"' % (ct, child_id[:20], ctext[:80]))

        # Check for Board in child
        if ct == 43:
            board_token = cb.get('board', {}).get('token', '')
            print('  *** BOARD TOKEN: %s' % board_token)
