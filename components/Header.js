import { signOut, signIn, useSession } from "next-auth/react";
import Link from "next/link";

export default function Header() {
  return (
    <div>
      <Link href={"/"}>Home</Link>
      <div>
        <AuthStatus />
      </div>
    </div>
  );
}

function AuthStatus() {
  const session = useSession();
  switch (session.status) {
    case "loading":
      return <>Loading...</>;
    case "authenticated":
      return (
        <>
          Signed in as {session.data.user?.email} <br />
          <button onClick={() => signOut()}>Sign out</button>
        </>
      );
    case "unauthenticated":
      return (
        <>
          Not signed in <br />
          <button onClick={() => signIn("fusionauth")}>Sign in</button>
        </>
      );
  }
}
