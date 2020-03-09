class BaseModel:
    _sub_model = {}  # key: container_type, type

    __ignore_attrs = ['data', 'model_attrs']
    _ignore_load_attrs = []
    _ignore_dump_attrs = []

    def is_property(self, attr):
        return isinstance(getattr(self.__class__, attr, None), property)

    @property
    def model_attrs(self):
        attrs = dir(self)
        ks_cls = dir(self.__class__)
        for attr in ks_cls:
            if not self.is_property(attr):
                attrs.remove(attr)
        for attr in attrs:
            if attr[0] == '_' or attr in self.__ignore_attrs:
                attrs.remove(attr)
        return attrs

    def _data(self, convert_sub_model=True, remove_property=True):
        data = {}
        for k in self.model_attrs:
            if k in self._ignore_dump_attrs or k in self.__ignore_attrs or (remove_property and self.is_property(k)):
                continue

            v = getattr(self, k)
            if convert_sub_model:
                if isinstance(v, BaseModel):
                    v = v.data
                else:
                    if k in self._sub_model:
                        sub_model = self._sub_model[k]
                        if isinstance(sub_model, tuple):
                            c_type, type = sub_model
                            if c_type == list:
                                items = [v_.data for v_ in v]
                                v = items
                            elif c_type == dict:
                                items = dict([(k_, v_.data) for k_, v_ in v.items()])
                                v = items
                            else:
                                raise Exception('Unsupport Type.')
                        elif issubclass(sub_model, BaseModel):
                            v = v.data
            if not callable(v):
                data[k] = v
        return data

    @property
    def data(self):
        return self._data()

    def load_data(self, **kwargs):
        for k in self.model_attrs:
            v = kwargs.get(k)
            if k in self._ignore_load_attrs or k in self.__ignore_attrs or v is None or self.is_property(k):
                continue

            if k in self._sub_model:
                sub_model = self._sub_model[k]
                if isinstance(sub_model, tuple):
                    c_type, v_type = sub_model
                    if c_type == list:
                        items = []
                        for i in v:
                            if isinstance(i, v_type):
                                item = i
                            else:
                                item = v_type()  # type: BaseModel
                                item.load_data(**i)
                            items.append(item)
                        v = items
                    elif c_type == dict:
                        items = {}
                        for k_, v_ in v.items():
                            if isinstance(v_, v_type):
                                item = v_
                            else:
                                item = v_type()  # type: BaseModel
                                item.load_data(**v_)
                            items[k_] = item
                        v = items
                    else:
                        raise Exception('Unsupport Type.')
                elif issubclass(sub_model, BaseModel):
                    model = sub_model()
                    model.load_data(**v)
                    v = model

            if hasattr(self, k):
                setattr(self, k, v)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, ('%a' % self._data(False, False))[1:-1])
