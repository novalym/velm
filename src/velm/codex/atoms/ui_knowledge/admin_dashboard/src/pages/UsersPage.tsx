import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export default function UsersPage() {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">Users</h3>
        <p className="text-sm text-muted-foreground">Manage system access and roles.</p>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Role</TableHead>
              <TableHead className="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell className="font-medium">Alice Smith</TableCell>
              <TableCell><Badge variant="default">Active</Badge></TableCell>
              <TableCell>Admin</TableCell>
              <TableCell className="text-right">$250.00</TableCell>
            </TableRow>
            <TableRow>
              <TableCell className="font-medium">Bob Jones</TableCell>
              <TableCell><Badge variant="destructive">Inactive</Badge></TableCell>
              <TableCell>Editor</TableCell>
              <TableCell className="text-right">$120.00</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>
  );
}