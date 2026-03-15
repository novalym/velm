import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DollarSign, Users, Activity, CreditCard } from "lucide-react";

export function StatsCards() {
  const stats = [
    { title: "Total Revenue", value: "$45,231.89", icon: DollarSign, desc: "+20.1% from last month" },
    { title: "Subscriptions", value: "+2350", icon: Users, desc: "+180.1% from last month" },
    { title: "Active Now", value: "+573", icon: Activity, desc: "+201 since last hour" },
    { title: "Sales", value: "+12,234", icon: CreditCard, desc: "+19% from last month" },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
            <stat.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground">{stat.desc}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}