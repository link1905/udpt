import {
  Header as MantineHeader,
  Autocomplete,
  Group,
  Burger,
  Box,
  Avatar,
  Container,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { IconSearch } from "@tabler/icons-react";

export function Header() {
  const [opened, { toggle }] = useDisclosure(false);

  return (
    <MantineHeader height={56} mb={120}>
      <Container size="xl" p="xs">
        <Group>
          <Group>
            <Burger opened={opened} onClick={toggle} size="sm" />
            LOGO
          </Group>
          <Group sx={{ flexGrow: 1, justifyContent: "center" }} align="center">
            <Autocomplete
              sx={{ width: 600 }}
              placeholder="Search"
              icon={<IconSearch size="1rem" stroke={1.5} />}
              data={[
                "React",
                "Angular",
                "Vue",
                "Next.js",
                "Riot.js",
                "Svelte",
                "Blitz.js",
              ]}
            />
          </Group>
          <Box>
            <Avatar color="cyan" radius="xl">
              MK
            </Avatar>
          </Box>
        </Group>
      </Container>
    </MantineHeader>
  );
}
