from textwrap import dedent
from typing import List, Tuple

from .registry import ComponentRegistry


@ComponentRegistry.register("auth-form")
def forge_auth_form(name: str, props: List[Tuple[str, str]]) -> str:
    # This artisan forges a complete, stateful login/signup form organism.
    return dedent(r'''
'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

export function AuthForm({ className }: { className?: string }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => setIsLoading(false), 1500);
  };

  return (
    <Tabs defaultValue="login" className={cn("w-[400px]", className)}>
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="login">Login</TabsTrigger>
        <TabsTrigger value="signup">Sign Up</TabsTrigger>
      </TabsList>
      <TabsContent value="login">
        <Card>
          <CardHeader>
            <CardTitle>Login to the Citadel</CardTitle>
            <CardDescription>Enter your credentials to access the Gnostic realm.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email-login">Email</Label>
              <Input id="email-login" type="email" placeholder="architect@scaffold.dev" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password-login">Password</Label>
              <Input id="password-login" type="password" required />
            </div>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={handleSubmit} disabled={isLoading}>
              {isLoading ? "Authenticating..." : "Enter the Citadel"}
            </Button>
          </CardFooter>
        </Card>
      </TabsContent>
      <TabsContent value="signup">
        <Card>
          <CardHeader>
            <CardTitle>Forge an Identity</CardTitle>
            <CardDescription>Create your new identity to begin your Great Work.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
             <div className="space-y-2">
              <Label htmlFor="name-signup">Name</Label>
              <Input id="name-signup" placeholder="The Architect" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email-signup">Email</Label>
              <Input id="email-signup" type="email" placeholder="architect@scaffold.dev" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password-signup">Password</Label>
              <Input id="password-signup" type="password" required />
            </div>
          </CardContent>
          <CardFooter>
            <Button className="w-full" onClick={handleSubmit} disabled={isLoading}>
              {isLoading ? "Forging..." : "Create Identity"}
            </Button>
          </CardFooter>
        </Card>
      </TabsContent>
    </Tabs>
  );
}
''')