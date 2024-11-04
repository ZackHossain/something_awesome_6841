from pathlib import Path
from typing import Optional
from sqlalchemy import Connection, Engine, URL, create_engine


class SQLEngine:
    """
    A class representing a SQL engine for connecting to a database.

    Attributes:
        driver (Optional[str]): The name of the database driver.
        host (Optional[str]): The hostname or IP address of the database server.
        database (Optional[str]): The name of the database.
        query (Optional[dict[str, str]]): A dictionary of query parameters.
        url (URL): The SQLAlchemy URL object representing the connection URL.
        engine (Engine): The SQLAlchemy Engine object representing the database engine.

    Methods:
        connect() -> Connection:
            Connects to the database using the configured engine and returns a SQLAlchemy Connection object.

    Note:
        This class requires the SQLAlchemy library to be installed.
    """
    def __init__(
            self,
            driver: Optional[str],
            host: Optional[str],
            database: Optional[str], query: Optional[dict[str, str]],
            **kwargs
    ) -> None:
        self.driver = driver
        self.host = host
        self.database = database
        self.query = query

        self.url = URL.create(
            drivername=self.driver,
            host=self.host,
            database=self.database,
            query=self.query,
            **kwargs  # type: ignore
        )

        self.engine = create_engine(url=self.url)

    def connect(self) -> Connection:
        return self.engine.connect()


class MSSQLEngine(SQLEngine):
    """
    A class that represents a Microsoft SQL Server Engine.

    Attributes:
        driver (str): The driver to connect to the SQL Server (default: "mssql+pyodbc").
        query (dict[str, str]): The query to connect to the SQL Server (default: {"driver": "SQL Server Native Client 11.0"})

    Methods:
        __init__(host: str, database: str, **kwargs) -> None: Initializes the MSSQLEngine instance with the given host, database, and additional **kwargs.

    """
    driver: str = "mssql+pyodbc"
    query: dict[str, str] = {"driver": "SQL Server Native Client 11.0"}

    def __init__(self, host: str, database: str, **kwargs) -> None:
        super().__init__(
            driver=self.driver,
            host=host,
            database=database,
            query=self.query,
            **kwargs  # type: ignore
        )


class AccessEngine(SQLEngine):
    """

    Module implementing the AccessEngine class.

    The AccessEngine class is a subclass of SQLEngine and provides methods to interact with a Microsoft Access database.

    """
    driver: str = "access+pyodbc"
    query: dict[str, str] = {
        "driver": "Microsoft Access Driver (*.mdb, *.accdb)",
        "ExtendedAnsiSql": "1"
    }

    def __init__(self, db_path: str | Path, **kwargs) -> None:
        self.query["DBQ"] = str(Path(db_path).absolute())
        super().__init__(
            driver=self.driver,
            host=None,
            database=None,
            query=self.query,
            **kwargs  # type: ignore
        )


def build_engine(
        driver: str = None,
        host: str = None,
        database: str = None,
        query: dict[str, str] = None,
        local_db_filepath: str | Path = None,
        **kwargs
) -> Engine:
    """
    Args:
        driver (str): The driver to use for the database connection.
        host (str): The host address of the database server.
        database (str): The name of the database to connect to.
        query (dict[str, str]): A dictionary of query parameters for the database connection.
        local_db_filepath (str | Path): The filepath of the local database file. Only required when using the 'access' driver.
        **kwargs: Additional keyword arguments to pass to the engine.

    Returns:
        Engine: The SQLAlchemy engine object for the database connection.

    Raises:
        AssertionError: When neither driver nor local_db_filepath is specified.
        Exception: If any exception occurs during the engine creation process.
    """
    assert driver is not None or local_db_filepath is not None, "Specify a driver or local database file path."
    try:
        if driver == "mssql":
            return MSSQLEngine(
                host=host,
                database=database,
                **kwargs  # type: ignore
            ).engine

        elif driver == "access":
            assert local_db_filepath is not None, "Using Access you must specify a local database file path."
            return AccessEngine(
                db_path=local_db_filepath,
                **kwargs  # type: ignore
            ).engine

        else:
            return SQLEngine(
                driver=driver,
                host=host,
                database=database,
                query=query,
                **kwargs  # type: ignore
            ).engine
    except Exception as e:
        raise e
