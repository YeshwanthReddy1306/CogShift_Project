try:
    import rotation_utils as _ru
    _CPP = True
except ImportError:
    _CPP = False

def torque_ratio(r1: float, r2: float) -> float:
    if _CPP:
        return _ru.torque_ratio(r1, r2)
    if r2 == 0:
        raise ValueError("r2 must be non-zero")
    return r1 / r2

def propagate_directions(node_count, edges, source_idx, source_dir):
    if _CPP:
        return list(_ru.propagate_directions(node_count, edges, source_idx, source_dir))
    from collections import deque
    adj = {i: [] for i in range(node_count)}
    for i in range(0, len(edges), 2):
        a, b = edges[i], edges[i+1]
        adj[a].append(b)
        adj[b].append(a)
    dirs    = [0] * node_count
    visited = [False] * node_count
    dirs[source_idx]    = source_dir
    visited[source_idx] = True
    q = deque([source_idx])
    while q:
        cur = q.popleft()
        for nb in adj[cur]:
            if not visited[nb]:
                visited[nb] = True
                dirs[nb] = -dirs[cur]
                q.append(nb)
    return dirs
