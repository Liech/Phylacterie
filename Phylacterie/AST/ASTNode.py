class ASTNode(object):
    def dump(self, indent=0):
        raise NotImplementedError

    def isScope(self):
      return False;