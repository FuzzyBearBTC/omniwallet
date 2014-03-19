import json
import threading

class StatsFileBackend:
  """
  This is a implementation of the Stats backend used to store the stats
  in a simple file. You can change this to a sql backend at a later date
  if needed.
  """
  def __init__(self, options=None):
    if options is None:
      options = {}
    self.lock = threading.Lock()
    self.db_path = options["db_path"]
    try:
      with open(self.db_path, "r") as f:
          self.stats = json.loads(f.read())
    except (ValueError, IOError) as e:
      self.stats = {}
      print "Could not read config, creating new one: " , e

    print "Saving stats in", self.db_path

  def persist(self):
    with open(self.db_path, "w") as f:
        f.write( json.dumps(self.stats) )

  def get(self, key):
    try:
      return self.stats[key] 
    except KeyError:
      return None

  def put(self, key, val):
    with self.lock:
      self.stats[key] = val
      self.persist()
