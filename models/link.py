class Link(object):

    def __init__(self, src, dst):
        """

        :param src (Port):
        :param dst (Port):
        :return:
        """
        self.src_port = src
        self.dst_port = dst

        src.link = self
        dst.link = self

        print("add link between {0} {1}".format(src.switch.id, dst.switch.id))

    def otherside(self, port):
        if self.src_port == port:
            return self.dst_port
        return self.src_port