import React, { useState } from 'react';

const Pagination = ({ UserPerPage, totalUsers, paginate }) => {

    const pageNumbers = [];

    for (let i = 1; i <= Math.ceil(totalUsers / UserPerPage); i++) {
        pageNumbers.push(i);
    }
    
    const [activeLink, setActiveLink] = useState(null);

    const [activeId, setActiveId] = useState(1);

    const handleClick = (id) => {
        setActiveLink(id);
    };
    return (
        <nav>
            <ul className='pagination d-flex mt-2 border-0' style={{display: "flex", justifyContent: "flex-end", cursor: "pointer"}}>
                {pageNumbers.map(number => (
                    <li key={number} onClick={() => setActiveId(number)} className={" " + (activeId === number ? "text-primary" : "") }>
                        <a onClick={() => paginate(number)} className='page-link'>
                            {number}
                        </a>
                    </li>
                ))}
            </ul>
        </nav>
    );
};

export default Pagination;