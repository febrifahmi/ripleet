# This Python file uses the following encoding: utf-8
# Combined from many sources by: @febrifahmi
import os
import requests
import settings
import socks
import socket
import time
import re
from datetime import date, datetime
from elasticsearch import Elasticsearch

# Get terminal size for the purpose of printing data on console
def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])

# get current unix timestamp (in seconds since the epoch time which is 1 january 1970)
def gettimeNow():
	now = int(time.time())
	return now

# get datetime object
def getdatetimenow():
	datetimenow = datetime.now()
	formatteddatetime = datetimenow.strftime("%Y-%m-%d %H:%M:%S")
	return formatteddatetime

# get today's date
def gettodaysdate():
	today = date.today()
	formatteddate = today.strftime("%Y-%m-%d")
	return formatteddate

# initiate Elasticsearch connection
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print(' [+] Connecting to Elasticsearch.. Yay Connect!')
        return _es
    else:
        print(' [x] Awww it could not connect to Elasticsearch!')

# create index in Elasticsearch with certain schema if not exists for storing news article data
def create_index_news(es_object, index_name):
	created = False
    # index settings for storing news article data
	settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
        	"properties": {
	        	"newstitle": {
		        	"type": "text"
	        	},
	        	"newsurl": {
		        	"type": "text"
	        	},
	        	"newstag": {
		        	"type": "keyword"
	        	},
	        	"newspubdate": {
		        	"type": "date"
	        	},
	        	"newscontent": {
		        	"type": "text"
	        	},
	        	"newsportal": {
		        	"type": "keyword"
				}
			}
		}
	}
	try:
		if not es_object.indices.exists(index_name):
			es_object.indices.create(index=index_name, ignore=400, body=settings)
			print(' [+] Created Index (Successful).')
		else:
			print(' [x] Index exists. Continuing..')
		created = True
	except Exception as ex:
		print(str(ex))
	finally:
		return created
	# try:
	# 	if not es_object.indices.exists(index_name):
	# 		# Ignore 400 means to ignore "Index Already Exist" error.
	# 		es_object.indices.create(index=index_name, ignore=400, body=settings)
	# 		print(' [+] Created Index (Successful).')
	# 	else:
	# 		print(' [+] Index exists. Continuing..')
	# 	created = True
	# except Exception as ex:
	# 	print(str(ex))
	# finally:
	# 	return created

# create index in Elasticsearch with certain schema if not exists for storing tweet data
def create_index_tweet(es_object, index_name):
    created = False
    # index settings, custom mapping adapted from https://gist.github.com/christinabo/6f849895e7df1e94a4fd450f7bf601e3
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
		    "properties": {
		      "coordinates": {
		        "properties": {
		          "coordinates": {
		            "type": "geo_point"
		          },
		          "type": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          }
		        }
		      },
		      "created_at": {
		        "type": "date",
		        "format": "EEE MMM dd HH:mm:ss Z yyyy"
		      },
		      "text": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }

		      },
		      "extended_tweet":{
		      	"properties":{
		      	  "full_text":{
		      	     "type": "text",
		      	     "fields": {
		      	       "keyword": {
		      	         "type": "keyword",
		      	         "ignore_above": 280
		      	       }
		      	     }
		      	  }

		      	}
		      },
		      "source": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "quote_count": {
		        "type": "long"
		      },
		      "reply_count": {
		        "type": "long"
		      },
		      "retweet_count": {
		        "type": "long"
		      },
		      "favorite_count": {
		        "type": "long"
		      },
		      "entities": {
		        "properties": {
		          "hashtags": {
		            "properties": {
		              "indices": {
		                "type": "long"
		              },
		              "text": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "media": {
		            "properties": {
		              "display_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "expanded_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "id": {
		                "type": "long"
		              },
		              "id_str": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "indices": {
		                "type": "long"
		              },
		              "media_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "media_url_https": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "sizes": {
		                "properties": {
		                  "large": {
		                    "properties": {
		                      "h": {
		                        "type": "long"
		                      },
		                      "resize": {
		                        "type": "text",
		                        "fields": {
		                          "keyword": {
		                            "type": "keyword",
		                            "ignore_above": 256
		                          }
		                        }
		                      },
		                      "w": {
		                        "type": "long"
		                      }
		                    }
		                  },
		                  "medium": {
		                    "properties": {
		                      "h": {
		                        "type": "long"
		                      },
		                      "resize": {
		                        "type": "text",
		                        "fields": {
		                          "keyword": {
		                            "type": "keyword",
		                            "ignore_above": 256
		                          }
		                        }
		                      },
		                      "w": {
		                        "type": "long"
		                      }
		                    }
		                  },
		                  "small": {
		                    "properties": {
		                      "h": {
		                        "type": "long"
		                      },
		                      "resize": {
		                        "type": "text",
		                        "fields": {
		                          "keyword": {
		                            "type": "keyword",
		                            "ignore_above": 256
		                          }
		                        }
		                      },
		                      "w": {
		                        "type": "long"
		                      }
		                    }
		                  },
		                  "thumb": {
		                    "properties": {
		                      "h": {
		                        "type": "long"
		                      },
		                      "resize": {
		                        "type": "text",
		                        "fields": {
		                          "keyword": {
		                            "type": "keyword",
		                            "ignore_above": 256
		                          }
		                        }
		                      },
		                      "w": {
		                        "type": "long"
		                      }
		                    }
		                  }
		                }
		              },
		              "source_status_id": {
		                "type": "long"
		              },
		              "source_status_id_str": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "type": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "symbols": {
		            "properties": {
		              "indices": {
		                "type": "long"
		              },
		              "text": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "urls": {
		            "properties": {
		              "display_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "expanded_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "indices": {
		                "type": "long"
		              },
		              "url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "user_mentions": {
		            "properties": {
		              "id": {
		                "type": "long"
		              },
		              "id_str": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "indices": {
		                "type": "long"
		              },
		              "name": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "screen_name": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          }
		        }
		      },
		      "favorite_count": {
		        "type": "long"
		      },
		      "favorited": {
		        "type": "boolean"
		      },
		      "filter_level": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "geo": {
		        "properties": {
		          "coordinates": {
		            "type": "float"
		          },
		          "type": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          }
		        }
		      },
		      "id": {
		        "type": "long"
		      },
		      "id_str": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "in_reply_to_screen_name": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "in_reply_to_status_id": {
		        "type": "long"
		      },
		      "in_reply_to_status_id_str": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "in_reply_to_user_id": {
		        "type": "long"
		      },
		      "in_reply_to_user_id_str": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "lang": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "place": {
		        "properties": {
		          "attributes": {
		            "properties": {
		              "street_address": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "bounding_box": {
		            "type": "geo_shape",
		            "coerce": "true",
		            "ignore_malformed": "true"
		          },
		          "country": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "country_code": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "full_name": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "id": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "name": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "place_type": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "url": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          }
		        }
		      },
		      "possibly_sensitive": {
		        "type": "boolean"
		      },
		      "retweet_count": {
		        "type": "long"
		      },
		      "retweeted": {
		        "type": "boolean"
		      },
		      "retweeted_status": {
		        "properties": {
		          "coordinates": {
		            "properties": {
		              "coordinates": {
		                "type": "float"
		              },
		              "type": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "created_at": {
		            "type": "date",
		            "format": "EEE MMM dd HH:mm:ss Z yyyy"
		          },
		          "entities": {
		            "properties": {
		              "hashtags": {
		                "properties": {
		                  "indices": {
		                    "type": "long"
		                  },
		                  "text": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  }
		                }
		              },
		              "media": {
		                "properties": {
		                  "display_url": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "expanded_url": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "id": {
		                    "type": "long"
		                  },
		                  "id_str": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "indices": {
		                    "type": "long"
		                  },
		                  "media_url": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "media_url_https": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "sizes": {
		                    "properties": {
		                      "large": {
		                        "properties": {
		                          "h": {
		                            "type": "long"
		                          },
		                          "resize": {
		                            "type": "text",
		                            "fields": {
		                              "keyword": {
		                                "type": "keyword",
		                                "ignore_above": 256
		                              }
		                            }
		                          },
		                          "w": {
		                            "type": "long"
		                          }
		                        }
		                      },
		                      "medium": {
		                        "properties": {
		                          "h": {
		                            "type": "long"
		                          },
		                          "resize": {
		                            "type": "text",
		                            "fields": {
		                              "keyword": {
		                                "type": "keyword",
		                                "ignore_above": 256
		                              }
		                            }
		                          },
		                          "w": {
		                            "type": "long"
		                          }
		                        }
		                      },
		                      "small": {
		                        "properties": {
		                          "h": {
		                            "type": "long"
		                          },
		                          "resize": {
		                            "type": "text",
		                            "fields": {
		                              "keyword": {
		                                "type": "keyword",
		                                "ignore_above": 256
		                              }
		                            }
		                          },
		                          "w": {
		                            "type": "long"
		                          }
		                        }
		                      },
		                      "thumb": {
		                        "properties": {
		                          "h": {
		                            "type": "long"
		                          },
		                          "resize": {
		                            "type": "text",
		                            "fields": {
		                              "keyword": {
		                                "type": "keyword",
		                                "ignore_above": 256
		                              }
		                            }
		                          },
		                          "w": {
		                            "type": "long"
		                          }
		                        }
		                      }
		                    }
		                  },
		                  "source_status_id": {
		                    "type": "long"
		                  },
		                  "source_status_id_str": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "type": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "url": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  }
		                }
		              },
		              "urls": {
		                "properties": {
		                  "display_url": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "expanded_url": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "indices": {
		                    "type": "long"
		                  },
		                  "url": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  }
		                }
		              },
		              "user_mentions": {
		                "properties": {
		                  "id": {
		                    "type": "long"
		                  },
		                  "id_str": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "indices": {
		                    "type": "long"
		                  },
		                  "name": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  },
		                  "screen_name": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  }
		                }
		              }
		            }
		          },
		          "favorite_count": {
		            "type": "long"
		          },
		          "favorited": {
		            "type": "boolean"
		          },
		          "filter_level": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "geo": {
		            "properties": {
		              "coordinates": {
		                "type": "float"
		              },
		              "type": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "id": {
		            "type": "long"
		          },
		          "id_str": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "in_reply_to_screen_name": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "in_reply_to_status_id": {
		            "type": "long"
		          },
		          "in_reply_to_status_id_str": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "in_reply_to_user_id": {
		            "type": "long"
		          },
		          "in_reply_to_user_id_str": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "lang": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "place": {
		            "properties": {
		              "attributes": {
		                "properties": {
		                  "street_address": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  }
		                }
		              },
		              "bounding_box": {
		                "properties": {
		                  "coordinates": {
		                    "type": "float"
		                  },
		                  "type": {
		                    "type": "text",
		                    "fields": {
		                      "keyword": {
		                        "type": "keyword",
		                        "ignore_above": 256
		                      }
		                    }
		                  }
		                }
		              },
		              "country": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "country_code": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "full_name": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "id": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "name": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "place_type": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              }
		            }
		          },
		          "possibly_sensitive": {
		            "type": "boolean"
		          },
		          "retweet_count": {
		            "type": "long"
		          },
		          "retweeted": {
		            "type": "boolean"
		          },
		          "scopes": {
		            "properties": {
		              "followers": {
		                "type": "boolean"
		              }
		            }
		          },
		          "source": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "text": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "truncated": {
		            "type": "boolean"
		          },
		          "user": {
		            "properties": {
		              "contributors_enabled": {
		                "type": "boolean"
		              },
		              "created_at": {
		                "type": "date",
		                "format": "EEE MMM dd HH:mm:ss Z yyyy"
		              },
		              "default_profile": {
		                "type": "boolean"
		              },
		              "default_profile_image": {
		                "type": "boolean"
		              },
		              "description": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "favourites_count": {
		                "type": "long"
		              },
		              "followers_count": {
		                "type": "long"
		              },
		              "friends_count": {
		                "type": "long"
		              },
		              "geo_enabled": {
		                "type": "boolean"
		              },
		              "id": {
		                "type": "long"
		              },
		              "id_str": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "is_translator": {
		                "type": "boolean"
		              },
		              "lang": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "listed_count": {
		                "type": "long"
		              },
		              "location": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "name": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_background_color": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_background_image_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_background_image_url_https": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_background_tile": {
		                "type": "boolean"
		              },
		              "profile_banner_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_image_url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_image_url_https": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_link_color": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_sidebar_border_color": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_sidebar_fill_color": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_text_color": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "profile_use_background_image": {
		                "type": "boolean"
		              },
		              "protected": {
		                "type": "boolean"
		              },
		              "screen_name": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "statuses_count": {
		                "type": "long"
		              },
		              "time_zone": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "url": {
		                "type": "text",
		                "fields": {
		                  "keyword": {
		                    "type": "keyword",
		                    "ignore_above": 256
		                  }
		                }
		              },
		              "utc_offset": {
		                "type": "long"
		              },
		              "verified": {
		                "type": "boolean"
		              }
		            }
		          }
		        }
		      },
		      "scopes": {
		        "properties": {
		          "place_ids": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          }
		        }
		      },
		      "source": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "text": {
		        "type": "text",
		        "fields": {
		          "keyword": {
		            "type": "keyword",
		            "ignore_above": 256
		          }
		        }
		      },
		      "truncated": {
		        "type": "boolean"
		      },
		      "user": {
		        "properties": {
		          "contributors_enabled": {
		            "type": "boolean"
		          },
		          "created_at": {
		            "type": "date",
		            "format": "EEE MMM dd HH:mm:ss Z yyyy"
		          },
		          "default_profile": {
		            "type": "boolean"
		          },
		          "default_profile_image": {
		            "type": "boolean"
		          },
		          "derived": {
		            "properties": {
		              "geo": {
		                "properties": {
		                  "coordinates": {
		                    "type": "geo_point"
		                  }
		                }
		              }
		            }
		          },
		          "description": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "favourites_count": {
		            "type": "long"
		          },
		          "followers_count": {
		            "type": "long"
		          },
		          "friends_count": {
		            "type": "long"
		          },
		          "geo_enabled": {
		            "type": "boolean"
		          },
		          "id": {
		            "type": "long"
		          },
		          "id_str": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "is_translator": {
		            "type": "boolean"
		          },
		          "lang": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "listed_count": {
		            "type": "long"
		          },
		          "location": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "name": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_background_color": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_background_image_url": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_background_image_url_https": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_background_tile": {
		            "type": "boolean"
		          },
		          "profile_banner_url": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_image_url": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_image_url_https": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_link_color": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_sidebar_border_color": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_sidebar_fill_color": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_text_color": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "profile_use_background_image": {
		            "type": "boolean"
		          },
		          "protected": {
		            "type": "boolean"
		          },
		          "screen_name": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "statuses_count": {
		            "type": "long"
		          },
		          "time_zone": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "url": {
		            "type": "text",
		            "fields": {
		              "keyword": {
		                "type": "keyword",
		                "ignore_above": 256
		              }
		            }
		          },
		          "utc_offset": {
		            "type": "long"
		          },
		          "verified": {
		            "type": "boolean"
		          }
		        }
		      }
		    }
		}
    }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print(' [+] Created Index (Successful).')
        else:
        	print(' [+] Index exists. Continuing..')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

# store index / indexing process
def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type="_doc", body=record)
        print outcome
    except Exception as ex:
        print(' [x] Error in indexing data', str(ex))

# using TOR network for scraping data
def ToRify():
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket
    currentip = requests.get("http://icanhazip.com").text
    # (width, height) = getTerminalSize()
    # print "_" * width
    print "ToRify Using IP Address: " + currentip
    # print "_" * width

# multi word replacement using word dictionary
# adapted from https://www.daniweb.com/programming/software-development/code/216636/multiple-word-replace-in-text-python
# str1 (string to be replaced), str2 (returned string)
# use: str2 = multiwordReplace(str1, wordDic) to call the function
wordDic = {
	'yg': 'yang',
	'lg': 'lagi',
	'gak': 'tidak',
	'nggak': 'tidak',
	'aja': 'saja',
	'skrg': 'sekarang',
	'jd': 'jadi',
	'bgs': 'bagus',
	'krn': 'karena',
	'sdh': 'sudah',
	'koq': 'kok',
	'utk': 'untuk',
	'klu': 'kalau',
	'gimana': 'bagaimana',
	'smua': 'semua',
	'dgn': 'dengan',
	'bhw': 'bahwa',
	'kalo': 'kalau',
	'klo': 'kalau',
	'jgn': 'jangan',
	'blh': 'boleh',
	'bkn': 'bukan',
	'kyk': 'kayak',
	'tdk': 'tidak'}

def multiwordReplace(text, wordDic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)