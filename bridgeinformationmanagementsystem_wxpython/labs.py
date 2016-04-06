class aha:
    maybe = 'outer'
    def __init__(self):
        pass

    def mu(self):
        result = 'mu'
        return result

    def hell(self):
        result = 'hello'
        aha.maybe = 'hell'
        return result

print aha.maybe
print aha().mu()
print aha().hell()
print aha.maybe