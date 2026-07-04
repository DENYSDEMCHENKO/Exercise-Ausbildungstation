def format_metrics(host_counter, status_by_day, system_metrics, top_n=10):
    lines = []


    lines.append("# HELP top_hosts_requests_total Requests per host (top N).")
    lines.append("# TYPE top_hosts_requests_total gauge")
    for host, count in host_counter.most_common(top_n):
        safe_host = host.replace('"', '\\"')
        lines.append(f'top_hosts_requests_total{{host="{safe_host}"}} {count}')
    lines.append("")


    lines.append("# HELP http_requests_by_day_total HTTP requests by status category and day.")
    lines.append("# TYPE http_requests_by_day_total counter")
    for day, categories in sorted(status_by_day.items()):
        for category, count in sorted(categories.items()):
            lines.append(
                f'http_requests_by_day_total{{day="{day}",code="{category}"}} {count}'
            )
    lines.append("")


    lines.append("# HELP host_cpu_usage_percent Current CPU usage percent.")
    lines.append("# TYPE host_cpu_usage_percent gauge")
    lines.append(f'host_cpu_usage_percent {system_metrics["cpu_percent"]}')
    lines.append("")

    lines.append("# HELP host_ram_usage_percent Current RAM usage percent.")
    lines.append("# TYPE host_ram_usage_percent gauge")
    lines.append(f'host_ram_usage_percent {system_metrics["ram_percent"]}')
    lines.append("")

    return "\n".join(lines)