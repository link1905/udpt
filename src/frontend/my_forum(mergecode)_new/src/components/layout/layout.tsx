import { AppShell, Container } from "@mantine/core";
import { Outlet } from "react-router-dom";
import { Header } from "./header.tsx";

export function Layout() {
  return (
    <AppShell
      padding="md"
      // navbar={
      //   <Navbar width={{ base: 300 }} height={500} p="xs">
      //     {/* Navbar content */}
      //   </Navbar>
      // }
      header={<Header />}
      // styles={(theme) => ({
      //   main: {
      //     backgroundColor:
      //       theme.colorScheme === "dark"
      //         ? theme.colors.dark[8]
      //         : theme.colors.gray[0],
      //   },
      // })}
    >
      <Container size="xl">
        <Outlet />
      </Container>
    </AppShell>
  );
}
