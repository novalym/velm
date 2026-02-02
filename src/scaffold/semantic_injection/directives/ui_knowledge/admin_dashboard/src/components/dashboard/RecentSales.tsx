import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function RecentSales() {
  return (
    <div className="space-y-8">
      {[1, 2, 3, 4, 5].map((i) => (
        <div className="flex items-center" key={i}>
          <Avatar className="h-9 w-9">
            <AvatarImage src={`https://i.pravatar.cc/150?u=${i}`} alt="Avatar" />
            <AvatarFallback>OM</AvatarFallback>
          </Avatar>
          <div className="ml-4 space-y-1">
            <p className="text-sm font-medium leading-none">Olivia Martin</p>
            <p className="text-sm text-muted-foreground">olivia.martin@email.com</p>
          </div>
          <div className="ml-auto font-medium">+$1,999.00</div>
        </div>
      ))}
    </div>
  );
}