# scaffold/semantic_injection/directives/ui_knowledge/charts.py

"""
=================================================================================
== THE ORACLE OF VISUALIZATION (V-Ω-CHARTS)                                    ==
=================================================================================
This artisan generates responsive, theme-aware chart wrappers.
It assumes the presence of 'recharts' in the project, the industry standard.
"""
from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("line-chart")
def forge_line_chart(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a responsive Line Chart component.
    """
    return dedent(f"""
        import React from 'react';
        import {{ Line, LineChart as ReLineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid }} from 'recharts';
        import {{ cn }} from '@/lib/utils';

        export interface {name}Props extends React.HTMLAttributes<HTMLDivElement> {{
          data: any[];
          xKey?: string;
          yKey?: string;
          color?: string;
        }}

        export function {name}({{ 
          className, 
          data, 
          xKey = "name", 
          yKey = "value", 
          color = "hsl(var(--primary))",
          ...props 
        }}: {name}Props) {{
          return (
            <div className={{cn("h-[350px] w-full", className)}} {{...props}}>
              <ResponsiveContainer width="100%" height="100%">
                <ReLineChart data={{data}}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis 
                    dataKey={{xKey}} 
                    stroke="#888888" 
                    fontSize={{12}} 
                    tickLine={{false}} 
                    axisLine={{false}} 
                  />
                  <YAxis 
                    stroke="#888888" 
                    fontSize={{12}} 
                    tickLine={{false}} 
                    axisLine={{false}} 
                    tickFormatter={{(value) => `$${{value}}`}} 
                  />
                  <Tooltip 
                    contentStyle={{{{ backgroundColor: 'hsl(var(--popover))', borderColor: 'hsl(var(--border))' }}}}
                    itemStyle={{{{ color: 'hsl(var(--popover-foreground))' }}}}
                  />
                  <Line 
                    type="monotone" 
                    dataKey={{yKey}} 
                    stroke={{color}} 
                    strokeWidth={{2}} 
                    dot={{false}}
                    activeDot={{{{ r: 8 }}}}
                  />
                </ReLineChart>
              </ResponsiveContainer>
            </div>
          );
        }}
    """).strip()

@ComponentRegistry.register("bar-chart")
def forge_bar_chart(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a responsive Bar Chart component.
    """
    return dedent(f"""
        import React from 'react';
        import {{ Bar, BarChart as ReBarChart, ResponsiveContainer, Tooltip, XAxis, YAxis }} from 'recharts';
        import {{ cn }} from '@/lib/utils';

        export interface {name}Props extends React.HTMLAttributes<HTMLDivElement> {{
          data: any[];
          xKey?: string;
          yKey?: string;
        }}

        export function {name}({{ 
          className, 
          data, 
          xKey = "name", 
          yKey = "total", 
          ...props 
        }}: {name}Props) {{
          return (
            <div className={{cn("h-[350px] w-full", className)}} {{...props}}>
              <ResponsiveContainer width="100%" height="100%">
                <ReBarChart data={{data}}>
                  <XAxis 
                    dataKey={{xKey}} 
                    stroke="#888888" 
                    fontSize={{12}} 
                    tickLine={{false}} 
                    axisLine={{false}} 
                  />
                  <YAxis 
                    stroke="#888888" 
                    fontSize={{12}} 
                    tickLine={{false}} 
                    axisLine={{false}} 
                    tickFormatter={{(value) => `$${{value}}`}} 
                  />
                  <Tooltip 
                    cursor={{{{ fill: 'hsl(var(--muted))', opacity: 0.3 }}}}
                    contentStyle={{{{ backgroundColor: 'hsl(var(--popover))', borderColor: 'hsl(var(--border))', borderRadius: '6px' }}}}
                  />
                  <Bar 
                    dataKey={{yKey}} 
                    fill="hsl(var(--primary))" 
                    radius={[4, 4, 0, 0]} 
                  />
                </ReBarChart>
              </ResponsiveContainer>
            </div>
          );
        }}
    """).strip()