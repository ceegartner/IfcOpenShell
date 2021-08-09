class Data:
    is_loaded = False
    resources = {}
    resource_times = {}

    @classmethod
    def purge(cls):
        cls.is_loaded = False
        cls.resources = {}
        cls.resource_times = {}

    @classmethod
    def load(cls, file):
        cls._file = file
        if not cls._file:
            return
        cls.load_resources()
        cls.load_resource_times()
        cls.is_loaded=True

    @classmethod
    def load_resources(cls):
        cls.resources = {}
        for resource in cls._file.by_type("IfcResource"):
            data = resource.get_info()
            del data["OwnerHistory"]
            data["IsNestedBy"] = []
            for rel in resource.IsNestedBy:
                [data["IsNestedBy"].append(o.id()) for o in rel.RelatedObjects]
            data["Nests"] = []
            for rel in resource.Nests:
                [data["Nests"].append(rel.RelatingObject.id())]
            data["ResourceOf"] = []
            for rel in resource.ResourceOf:
                [data["ResourceOf"].append(o.id()) for o in rel.RelatedObjects]
            data["HasContext"] = resource.HasContext[0].RelatingContext.id() if resource.HasContext else None
            if resource.Usage:
                data["Usage"] = data["Usage"].id()
            cls.resources[resource.id()] = data

    @classmethod
    def load_resource_times(cls):
        cls.resource_times = {}
        for resource_time in cls._file.by_type("IfcResourceTime"):
            data = resource_time.get_info()
            for key, value in data.items():
                if not value:
                    continue
                if "Start" in key or "Finish" in key or key == "StatusTime":
                    data[key] = ifcopenshell.util.date.ifc2datetime(value)
                elif "Work" in key or key =="LevelingDelay":
                    data[key] = ifcopenshell.util.date.ifc2datetime(value)
            cls.resource_times[resource_time.id()] = data
