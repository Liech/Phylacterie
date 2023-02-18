
class ClassContainer(object):
  def __init__(self):
    self._classes = {}

  def hasClass(self, name):
    return name in self._classes;
  def getClass(self, name):
    return self._classes[name];
  def registerClass(self, name, classData):      
      self._classes[name] = classData;
  def getClasses(self):
    return self._classes;
