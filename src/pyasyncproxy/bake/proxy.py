"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pyasyncproxy.common.Snowflake import Snowflake
from pyasyncproxy.context.ProxyIpCacheLocal import ProxyIpCacheLocal
from pyasyncproxy.context.ProxyIpPoolLocal import ProxyIpPoolLocal
from pyasyncproxy.model.dto.ProjectEnv import ProjectEnv
from pyasyncproxy.model.dto.ProxyAppContext import ProxyAppContext
from pyasyncproxy.model.dto.ProxyTree import ProxyRootTree
from pyasyncproxy.service.proxy.ProxySimpleEngineFactory import ProxySimpleEngineFactory
from pyasyncproxy.service.proxy.ProxySimpleNodeFactory import ProxySimpleNodeFactory
from pyasyncproxy.service.proxy.ProxySimpleService import ProxySimpleService

env = ProjectEnv()
snowflake = Snowflake(env.worker_id, env.data_center_id)
with env.proxy_path.open("r") as f:
    proxy_tree = ProxyRootTree.model_validate_json("".join(f.readlines()))
nodes_map = ProxySimpleNodeFactory().collect_nodes()
proxy_engine_factory = ProxySimpleEngineFactory(nodes_map)
ip_cache = ProxyIpCacheLocal()
ip_pool = ProxyIpPoolLocal()
proxy_engine = proxy_engine_factory.create_engine(proxy_tree)
app_ctx = ProxyAppContext(env=env, ip_cache=ip_cache, ip_pool=ip_pool, snowflake=snowflake)
service = ProxySimpleService(app_ctx, proxy_engine)
