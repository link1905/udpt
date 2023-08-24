import { PropsWithChildren } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  authRequestQueryKey,
  requestAuthRefresh,
} from "../../services/account/auth-refresh.ts";
import { LoadingOverlay } from "@mantine/core";
import { Navigate, useMatch } from "react-router-dom";
export function LoginGuard({ children }: PropsWithChildren<{}>) {
  const { error, isLoading, data } = useQuery(
    authRequestQueryKey,
    requestAuthRefresh,
    {
      retry: 0,
    },
  );

  const isAdminPage = useMatch({
    path: "/admin",
    end: false,
  });

  if (isLoading) {
    return <LoadingOverlay visible />;
  }
  if (error) {
    return <Navigate to="/signin" />;
  }
  if (isAdminPage && !data?.fields?.is_staff) {
    return <Navigate to="/" />;
  }

  return <>{children}</>;
}
