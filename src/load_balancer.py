import os

def load_balancer(connList):
  scoreList = []
  for connection in connList:
    status = connection.getServerStats()
    print(status)
    if not isinstance(status, str):
      cpuUtilScore = float(os.getenv("CLIENT_CPU_WEIGHTAGE")) * (float(status.cpuUtil))
      ramUtilScore = float(os.getenv("CLIENT_RAM_WEIGHTAGE")) * (float(status.ramPercent))
      storageUtil = float(status.usedMemory) / float(status.totalMemory) * 100
      storageUtilScore = float(os.getenv("CLIENT_RAM_WEIGHTAGE")) * storageUtil
      totalScore = cpuUtilScore + ramUtilScore + storageUtilScore
      scoreList.append((totalScore, connection))
  scoreList.sort(key=lambda tup: tup[0])
  replicationFactor = int(os.getenv("CLIENT_REPLICATION_FACTOR"))
  return scoreList[:replicationFactor]