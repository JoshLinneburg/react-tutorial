import NextAuth from "next-auth";
import FusionAuthProvider from "next-auth/providers/fusionauth";
import jwt from "jsonwebtoken";

export default NextAuth({
  providers: [
    FusionAuthProvider({
      id: "fusionauth",
      name: "FusionAuth",
      issuer: process.env.FUSIONAUTH_ISSUER,
      clientId: process.env.FUSIONAUTH_CLIENT_ID,
      clientSecret: process.env.FUSIONAUTH_CLIENT_SECRET,
      profile(profile) {
        return {
          id: profile.sub,
          name: `${profile.given_name} ${profile.family_name}`,
          email: profile.email,
          image: profile.picture,
        };
      },
    }),
  ],
  jwt: {
    // A secret to use for key generation - you should set this explicitly
    // Defaults to NextAuth.js secret if not explicitly specified.
    // This is used to generate the actual signingKey and produces a warning
    // message if not defined explicitly.
    secret: process.env.JWT_SECRET,
    encode: async ({ secret, token, maxAge }) => {
      const encodedToken = jwt.sign(token, secret, { algorithm: "HS512" });

      return encodedToken;
    },
    decode: async ({ secret, token, maxAge }) => {
      const verify = jwt.verify(token, secret);

      return verify;
    },
  },
  callbacks: {
    async session({ session, token }) {
      session.user.id = token.sub;
      session.user.roles = token.roles;
      return session;
    },
    async jwt({ token, profile }) {
      if (profile) {
        token.roles = profile.roles;
      }
      return token;
    },
  },
});
