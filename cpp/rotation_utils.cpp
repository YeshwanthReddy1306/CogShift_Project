#include <vector>
#include <queue>
#include <unordered_map>
#include <stdexcept>

double torque_ratio(double r1, double r2) {
    if (r2 == 0.0) throw std::invalid_argument("r2 must be non-zero");
    return r1 / r2;
}

std::vector<int> propagate_directions(int node_count,
                                      const std::vector<int>& edges,
                                      int source_idx, int source_dir) {
    std::unordered_map<int,std::vector<int>> adj;
    for (size_t i = 0; i+1 < edges.size(); i += 2) {
        adj[edges[i]].push_back(edges[i+1]);
        adj[edges[i+1]].push_back(edges[i]);
    }
    std::vector<int>  dirs(node_count, 0);
    std::vector<bool> vis(node_count, false);
    dirs[source_idx] = source_dir;
    vis[source_idx]  = true;
    std::queue<int> q;
    q.push(source_idx);
    while (!q.empty()) {
        int cur = q.front(); q.pop();
        for (int nb : adj[cur])
            if (!vis[nb]) { vis[nb]=true; dirs[nb]=-dirs[cur]; q.push(nb); }
    }
    return dirs;
}
