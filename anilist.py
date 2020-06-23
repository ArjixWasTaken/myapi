import requests
from io import StringIO
import json
from bs4 import BeautifulSoup
def search_anilist(search, max_results=10):
  query = """
  query ($id: Int, $page: Int, $search: String, $type: MediaType) {
      Page (page: $page, perPage: 10) {
          media (id: $id, search: $search, type: $type) {
              id
              idMal
              description(asHtml: false)
              title {
                  english
                  romaji
              }
              coverImage {
                  medium
              }
              bannerImage
              averageScore
              meanScore
              status
              episodes
              chapters
              externalLinks {
                  url
                  site
              }
              nextAiringEpisode {
                  timeUntilAiring
              }
          }
      }
  }
  """
  variables = {
      'search': search,
      'page': 1,
      'perPage': max_results,
      'type': 'ANIME'
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  io = StringIO(response.text)
  results = json.load(io)
  try:
    result_list = results['data']['Page']['media']
    final_result = []
    for anime in result_list:
      title = anime['title']['romaji']
      ani_id = anime['id']
      status = anime['status']
      thumbnail = anime['coverImage']['medium']
      episodes = anime['episodes']
      description = anime['description']
      link = f'https://anilist.co/anime/{ani_id}'
      entry = {"title": title, "anilist_id": ani_id, "link": link, "episodes": episodes, "status":status, "description": description, "picture": thumbnail}
      final_result.append(entry)
  except:
    final_result = results['errors'][0]['message']
    raise Exception(final_result)
  return final_result