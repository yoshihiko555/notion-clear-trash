from notion.client import NotionClient


def get_trash(client):
    query = {
      "type": "BlocksInSpace",
      "query": "",
      "filters": {
        "isDeletedOnly": True,
        "excludeTemplates": False,
        "isNavigableOnly": True,
        "requireEditPermissions": False,
        "ancestors": [],
        "createdBy": [],
        "editedBy": [],
        "lastEditedTime": {},
        "createdTime": {}
      },
      "sort": "Relevance",
      "limit": 1000,
      "spaceId": client.current_space.id,
      "source": "trash"
    }
    try:
        results = client.post('/api/v3/search', query)
        block_ids = results.json()['results']
        return [block_id['id'] for block_id in block_ids]
    except Exception as e:
        print('Get Trash Error!!')
        print(e)


def chunks (lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def delete_permanently(client, block_ids):
    for block_batch in chunks(block_ids, 10):
        try:
            client.post("/api/v3/deleteBlocks", {"blockIds": block_batch, "permanentlyDelete": True})
        except Exception as err:
            print('Delete Trash Error!!')
            print(err)
            print(block_batch)

if __name__== "__main__":
    token = input('Please enter your auth token: ')
    client = NotionClient(token_v2=token)

    block_ids = get_trash(client)
    delete_permanently(client, block_ids)

    print('Successfully cleared all trash blocks.')
