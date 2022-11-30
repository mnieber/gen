from dataclasses import dataclass

from moonleap import Resource
from moonleap.utils.fp import append_uniq


@dataclass
class Pipeline(Resource):
    pass


@dataclass
class PropsSource(Resource):
    pass


class PipelineData:
    def __init__(self):
        self.default_prop_items = list()
        self.default_prop_item_lists = list()
        self.prop_items = list()
        self.prop_item_lists = list()
        self.queries = list()
        self.mutations = list()

    def update(self, pipelines):
        for pipeline in pipelines:
            pipeline_source = pipeline.source
            if pipeline_source.meta.term.tag == "props":
                res = pipeline.resources[0]
                if res.meta.term.tag == "item":
                    self.prop_items.append(res.typ)
                elif res.meta.term.tag == "item~list":
                    self.prop_item_lists.append(res.typ)
            elif pipeline_source.meta.term.tag == "query":
                append_uniq(self.queries, pipeline_source)
            elif pipeline_source.meta.term.tag == "mutation":
                append_uniq(self.mutations, pipeline_source)
            elif pipeline_source.meta.term.tag == "item":
                append_uniq(self.default_prop_items, pipeline_source)
            elif pipeline_source.meta.term.tag == "item_list":
                append_uniq(self.default_prop_item_lists, pipeline_source)
            else:
                raise Exception("Unknown pipeline source")
