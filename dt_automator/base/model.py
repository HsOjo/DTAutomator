class BaseModel:
    _sub_model = {}  # key: container_type, type
    _ignore_attrs = []

    @property
    def data(self):
        data = {}
        ks = dir(self)
        for k in dir(self.__class__):
            ks.remove(k)
        for k in ks:
            if k[0] != '_' and k != 'data' and k not in self._ignore_attrs:
                v = getattr(self, k)
                if isinstance(v, BaseModel):
                    v = v.data
                if k in self._sub_model:
                    c_type, type = self._sub_model[k]
                    if c_type == list:
                        items = [v_.data for v_ in v]
                        v = items
                    elif c_type == dict:
                        items = dict([(k_, v_.data) for k_, v_ in v.items()])
                        v = items
                    else:
                        raise Exception('Unsupport Type.')

                if not callable(v):
                    data[k] = v
        return data

    def load_data(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._ignore_attrs:
                continue
            if k in self._sub_model:
                c_type, v_type = self._sub_model[k]
                if c_type == list:
                    items = []
                    for i in v:
                        item = v_type()  # type: BaseModel
                        item.load_data(**i)
                        items.append(item)
                    v = items
                elif c_type == dict:
                    items = {}
                    for k_, v_ in v.items():
                        item = v_type()  # type: BaseModel
                        item.load_data(**v_)
                        items[k_] = item
                    v = items
                else:
                    raise Exception('Unsupport Type.')
            if hasattr(self, k):
                setattr(self, k, v)
